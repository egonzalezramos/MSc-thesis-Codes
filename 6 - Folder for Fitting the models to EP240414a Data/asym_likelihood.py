"""Custom likelihoods for radio fitting workflows."""

import numpy as np
import redback as rd
from scipy.special import erf


class AsymGaussianWithUpperLimits(rd.likelihoods.GaussianLikelihoodWithUpperLimits):
    def __init__(
        self,
        x,
        y,
        sigma_lower,
        sigma_upper,
        function,
        kwargs=None,
        priors=None,
        fiducial_parameters=None,
        detections=None,
        upper_limit_sigma=3.0,
        data_mode="flux",
        unreliable_mask1=None,
        reliability_key1="f_rel1",
        unreliable_mask2=None,
        reliability_key2="f_rel2",
    ):
        #New Update: I added another f_sys, so we can have two datasets with different 
        #systematic errors at the same time.
        sigma_lower = np.asarray(sigma_lower, dtype=float)
        sigma_upper = np.asarray(sigma_upper, dtype=float)
        if len(sigma_lower) != len(x) or len(sigma_upper) != len(x):
            raise ValueError("sigma_lower/sigma_upper must have length len(x).")

        # Parent class requires one sigma array; keep conservative symmetric sigma.
        sigma_sym = np.maximum(sigma_lower, sigma_upper)
        super().__init__(
            x=x,
            y=y,
            sigma=sigma_sym,
            function=function,
            kwargs=kwargs,
            priors=priors,
            fiducial_parameters=fiducial_parameters,
            detections=detections,
            upper_limit_sigma=upper_limit_sigma,
            data_mode=data_mode,
        )

        self._model_parameter_keys = tuple(self.parameters.keys())
        self.sigma_lower = sigma_lower
        self.sigma_upper = sigma_upper
        self.reliability_key1 = reliability_key1
        self.reliability_key2 = reliability_key2
        # f_rel is treated as a fractional systematic term (>=0).
        self.parameters[self.reliability_key1] = 0.0
        self.parameters[self.reliability_key2] = 0.0

        if unreliable_mask2 is None:
            if unreliable_mask1 is None:
                unreliable_mask1 = np.ones(len(x), dtype=bool)
            unreliable_mask2=unreliable_mask1
        self.unreliable_mask1 = np.asarray(unreliable_mask1, dtype=bool)
        self.unreliable_mask2 = np.asarray(unreliable_mask2, dtype=bool)
        if len(self.unreliable_mask1) != len(x):
            raise ValueError("unreliable_mask1 must have length len(x).")
        if len(self.unreliable_mask2) != len(x):
            raise ValueError("unreliable_mask2 must have length len(x).")
    @property
    def model_output(self):
        model_params = {k: self.parameters[k] for k in self._model_parameter_keys}
        model_kwargs = dict(self.kwargs or {})
        # Some redback afterglow controls (e.g., k for ISM/WIND) are kwargs-only.
        #For considering lateral expansion we must also do this explicitly.
        # If they are fixed/sampled parameters, forward them explicitly.
        if "k" in self.parameters and "k" not in model_kwargs:
            model_kwargs["k"] = self.parameters["k"]
        return self.function(self.x, **model_params, **model_kwargs)

    def log_likelihood(self):
        f_rel1 = float(self.parameters.get(self.reliability_key1, 0.0))
        if f_rel1 < 0.0:
            return -np.inf
        f_rel2 = float(self.parameters.get(self.reliability_key2, 0.0))
        if f_rel2 < 0.0:
            return -np.inf

        # Add fractional systematic uncertainty in quadrature only on masked points.
        systematic = np.zeros(len(self.x), dtype=float)
        #Be careful! If both boolean arrays have elements in common the second one 
        #is going to overwrite the first one, so take this into account!
        systematic[self.unreliable_mask1] = f_rel1 * self.y[self.unreliable_mask1]
        systematic[self.unreliable_mask2] = f_rel2 * self.y[self.unreliable_mask2]
        s_minus = np.sqrt(self.sigma_lower**2 + systematic**2)
        s_plus = np.sqrt(self.sigma_upper**2 + systematic**2)
        model = self.model_output
        if np.any(~np.isfinite(model)):
            return -np.inf
        residual = self.y - model

        detections = np.asarray(self.detections, dtype=bool)
        upper_limits = np.asarray(self.upper_limits, dtype=bool)

        # Detections: split-normal likelihood.
        if np.any(detections):
            res = residual[detections]  # y - model
            sm = s_minus[detections]
            sp = s_plus[detections]
            if (
                np.any(sm <= 0)
                or np.any(sp <= 0)
                or np.any(~np.isfinite(sm))
                or np.any(~np.isfinite(sp))
                or np.any(~np.isfinite(res))
            ):
                return -np.inf
            s_side = np.where(res >= 0.0, sm, sp)
            ll_det = np.sum(
                np.log(np.sqrt(2.0 / np.pi))
                - np.log(sm + sp)
                - 0.5 * (res / s_side)**2
            )
        else:
            ll_det = 0.0

        # Upper limits: same CDF term as redback, with inflated uncertainty.
        if np.any(upper_limits):
            obs_ul = self.y[upper_limits]
            mod_ul = model[upper_limits]
            ul_sig_level = self.get_upper_limit_sigma_values()

            if self.data_mode == "magnitude":
                sigma_ul = np.full_like(obs_ul, 0.1, dtype=float)
                z = (obs_ul - mod_ul) / sigma_ul
                cdf = 1.0 - 0.5 * (1.0 + erf(z / np.sqrt(2.0)))
            else:
                sigma_ul = np.abs(obs_ul / ul_sig_level)
                sigma_ul = np.sqrt(sigma_ul**2 + systematic[upper_limits]**2)
                if (
                    np.any(sigma_ul <= 0)
                    or np.any(~np.isfinite(sigma_ul))
                    or np.any(~np.isfinite(obs_ul))
                    or np.any(~np.isfinite(mod_ul))
                ):
                    return -np.inf
                z = (obs_ul - mod_ul) / sigma_ul
                cdf = 0.5 * (1.0 + erf(z / np.sqrt(2.0)))

            ll_ul = np.sum(np.log(np.clip(cdf, 1e-300, 1.0)))
        else:
            ll_ul = 0.0

        return np.nan_to_num(ll_det + ll_ul, nan=-np.inf, neginf=-np.inf, posinf=-np.inf)

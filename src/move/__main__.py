__all__ = []

import hydra
from omegaconf import OmegaConf

import move.tasks
from move import HYDRA_VERSION_BASE
from move.conf.schema import (
    AnalyzeLatentConfig,
    EncodeDataConfig,
    IdentifyAssociationsConfig,
    MOVEConfig,
    TuneModelConfig,
)
from move.core.logging import get_logger

import move.tasks.analyze_latent_fast


@hydra.main(
    config_path="conf",
    config_name="main",
    version_base=HYDRA_VERSION_BASE,
)
def main(config: MOVEConfig) -> None:
    """Run MOVE.

    Example:
        $ python -m move experiment=random_small -cd=tutorial/config
    """
    if not hasattr(config, "task"):
        raise ValueError("No task defined.")
    task_type = OmegaConf.get_type(config.task)
    if task_type is None:
        logger = get_logger("move")
        logger.info("No task specified.")
    elif task_type is EncodeDataConfig:
        move.tasks.encode_data(config.data)
    elif issubclass(task_type, TuneModelConfig):
        move.tasks.tune_model(config)
    # the fast version  does not calcuate feature importance, it is only to look at the reconstruction metrics
    elif task_type is AnalyzeLatentConfig:
        if config.task.fast:
            move.tasks.analyze_latent_fast(config)
        else:
            move.tasks.analyze_latent(config)
    elif issubclass(task_type, IdentifyAssociationsConfig):
        if config.task.multiprocess:
            move.tasks.identify_associations_multiprocess(config)
        else:
            move.tasks.identify_associations(config)
        #What we had before
        #move.tasks.identify_associations(config)
    else:
        raise ValueError("Unsupported type of task.")


if __name__ == "__main__":
    main()

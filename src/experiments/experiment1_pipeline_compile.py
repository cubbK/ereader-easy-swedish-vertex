from kfp import compiler
from .experiment1_pipeline import pipeline


if __name__ == "__main__":
    compiler.Compiler().compile(
        pipeline_func=pipeline,  # type: ignore
        package_path="experiment1_pipeline.json",
    )

from diffusers import StableDiffusionXLPipeline
import torch


def get_pipeline():
    model_id = "stabilityai/stable-diffusion-xl-base-1.0"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    pipeline = StableDiffusionXLPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.float16,  # Use float16 for faster computation on GPUs
    )
    return pipeline.to(device)

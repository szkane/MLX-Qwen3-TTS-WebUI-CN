from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="mlx-community/chatterbox-turbo-fp16",
    local_dir="../models/Chatterbox-Turbo-FP16",
    local_dir_use_symlinks=False
)

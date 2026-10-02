import sys
from pathlib import Path
from PIL import Image, ImageSequence

SUPPORTED_EXTS = {".svg" ".png", ".jpg", ".jpeg", ".gif"}

def convert_image(image_path: Path):
    output_path = image_path.with_suffix(".webp")

    if output_path.exists():
        print(f"[SKIP] {output_path.relative_to(ROOT_DIR)}")
        return False

    try:
        with Image.open(image_path) as img:
            is_animated = getattr(img, "is_animated", False)

            if is_animated:
                frames = []
                durations = []

                for frame in ImageSequence.Iterator(img):
                    frames.append(frame.convert("RGBA"))
                    durations.append(frame.info.get("duration", 100))

                frames[0].save(
                    output_path,
                    format="WEBP",
                    save_all=True,
                    append_images=frames[1:],
                    duration=durations,
                    loop=img.info.get("loop", 0),
                    lossless=True
                )
            else:
                img.save(output_path, format="WEBP", lossless=True)

        print(f"[OK]   {image_path.relative_to(ROOT_DIR)}")
        return True

    except Exception as e:
        print(f"[ERR]  {image_path}: {e}")
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python utils/conv2webp.py <folder_from_root> [--recursive]")
        sys.exit(1)

    folder_arg = sys.argv[1]
    recursive = "--recursive" in sys.argv

    global ROOT_DIR
    ROOT_DIR = Path(__file__).resolve().parent.parent
    target_dir = ROOT_DIR / folder_arg

    if not target_dir.exists() or not target_dir.is_dir():
        print(f"[ERROR] Folder does not exist: {target_dir}")
        sys.exit(1)

    if recursive:
        files = [p for p in target_dir.rglob("*") if p.suffix.lower() in SUPPORTED_EXTS]
    else:
        files = [p for p in target_dir.iterdir() if p.is_file() and p.suffix.lower() in SUPPORTED_EXTS]

    if not files:
        print("[INFO] No supported images found.")
        return

    print(f"[INFO] Found {len(files)} image(s)")
    converted = 0

    for img in files:
        if convert_image(img):
            converted += 1

    print(f"[DONE] Converted {converted}/{len(files)} images")


if __name__ == "__main__":
    main()

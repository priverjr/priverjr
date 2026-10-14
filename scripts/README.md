# Profile artwork

The artwork consists of original graphics generated locally with Pillow. Its text remains visible throughout the animation, and it makes no requests to an external rendering service.

To regenerate on Linux with Fontconfig and Liberation Sans installed:

```sh
python -m pip install 'Pillow>=10,<13'
python scripts/generate_banner.py
```

The script creates a nine-second animated hero, a flowing divider, and four animated project cards, each with a static PNG companion. To use the still version, change `assets/profile-banner.gif` to `assets/profile-banner.png` in the root README.

Keep biography details, project descriptions and contact links in the root README up to date. The profile deliberately avoids external statistics cards that can become unavailable or display misleading counts.

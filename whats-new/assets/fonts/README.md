HyperFrames bundles Inter, Montserrat, Outfit, Nunito, Oswald, League Gothic, Archivo Black, Space Mono,
IBM Plex Mono, JetBrains Mono, EB Garamond, Playfair Display, Source Code Pro, Noto Sans JP, Roboto, Open Sans,
Lato and Poppins — set `brand.font` to one of those names and leave `brand.font_files` empty.

For any other face, put the files here and map weights in storyboard.json:
  "font": "Acme Sans", "font_files": { "600": "assets/fonts/AcmeSans-SemiBold.ttf", "900": "assets/fonts/AcmeSans-Black.ttf" }
The build writes the @font-face rules into every scene.

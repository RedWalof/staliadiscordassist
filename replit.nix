{pkgs}: {
  deps = [
    pkgs.ffmpeg_7-full
    pkgs.python310Full        # Utilise Python 3.10 ou plus récent
    pkgs.ffmpeg               # Ajoute FFmpeg
    pkgs.libopus              # Ajoute la bibliothèque Opus
    pkgs.yt-dlp               # Ajoute yt-dlp pour gérer les vidéos/audio
  ];
}

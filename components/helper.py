def get_base_url(m3u8_url):
    """Slice the provided M3U8 URL to generate the base URL."""
    return '/'.join(m3u8_url.split('/')[:-1]) + '/'


def camel_case_filename(filename):
    """Convert a given string filename to camelCase format."""
    words = filename.split()
    camel_cased_words = [words[0].lower()] + [word.capitalize() for word in words[1:]]
    return ''.join(camel_cased_words)


def format_size(size_in_bytes):
    """Converts the given size in bytes to a user-friendly string format."""
    size_in_mb = size_in_bytes / (1024 * 1024)

    # If size is larger than 1024 MB (i.e., 1 GB), convert it to GB
    if size_in_mb > 1024:
        size_in_gb = size_in_mb / 1024
        return f"{size_in_gb:.2f} GB"
    else:
        return f"{size_in_mb:.2f} MB"

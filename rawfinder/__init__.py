raw_extensions = [
    # --- Canon ---
    ".crw",  # Old Canon RAW format (before CR2)
    ".cr2",  # Canon RAW 2 (common in DSLRs until ~2018)
    ".cr3",  # Canon RAW 3 (newer DSLRs and mirrorless models)
    # --- Nikon ---
    ".nef",  # Nikon Electronic Format (main Nikon RAW)
    ".nrw",  # Nikon RAW (used by certain Coolpix and compact cameras)
    # --- Sony ---
    ".arw",  # Sony Alpha RAW (current primary format)
    ".srf",  # Sony RAW Format (older models)
    ".sr2",  # Sony RAW 2 (older DSLRs)
    # --- Fujifilm ---
    ".raf",  # Fujifilm RAW (X-series, GFX, etc.)
    # --- Panasonic ---
    ".rw2",  # Panasonic RAW (Lumix series)
    ".raw",  # Some older Panasonic models used ".raw" as extension
    # --- Olympus ---
    ".orf",  # Olympus RAW Format
    # --- Pentax ---
    ".pef",  # Pentax Electronic Format
    # Many Pentax models also support .dng
    # --- Ricoh ---
    # Ricoh acquired Pentax; some Ricoh cameras also produce .dng natively
    # --- Leica ---
    ".rwl",  # Leica RAW (certain lines/models)
    # Leica also heavily uses .dng
    # --- Sigma (Foveon sensors) ---
    ".x3f",  # Sigma RAW (sd, dp series)
    # --- Samsung ---
    ".srw",  # Samsung RAW (NX series)
    # --- Hasselblad ---
    ".3fr",  # Hasselblad RAW (modern format)
    ".fff",  # Older Imacon/Hasselblad format
    # --- Phase One ---
    ".iiq",  # Phase One (digital backs)
    # --- Leaf (part of Phase One) ---
    ".mos",  # Leaf RAW format
    # --- Minolta ---
    ".mrw",  # Minolta RAW (older cameras)
    # --- Kodak (historical DSLRs) ---
    ".dcr",  # Kodak DC RAW
    ".kdc",  # Kodak DC
    ".k25",  # Another historical Kodak RAW format
    # --- Epson ---
    ".erf",  # Epson RAW (R-D1)
    # --- Mamiya ---
    ".mef",  # Mamiya RAW (older digital backs)
    # --- Sinar ---
    ".sti",  # Sinar RAW (rarely encountered)
    # --- ARRI ---
    ".ari",  # ARRI RAW (used in ARRI Alexa and other cinema cameras)
    # --- Smartphones (Apple / Android) & Others: Adobe DNG ---
    ".dng",  # Open "universal" RAW format from Adobe
    # - Apple ProRAW (iPhone) uses .dng
    # - Many Android phones (e.g., Google Pixel) can produce .dng
    # - Leica, Pentax, Ricoh, Hasselblad also use .dng
]

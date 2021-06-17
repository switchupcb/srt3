"""srt tools perform tasks using the srt module."""
import os
import importlib

folder_path = os.path.normpath(os.path.join(__file__, os.pardir))
for file in os.listdir(folder_path):
    if not file.startswith("_"):
        importlib.import_module(f"srt.tools.tool.{file[:-3]}")
del folder_path
del file

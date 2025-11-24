# -*- coding: utf-8 -*-
import io
from datetime import datetime
import pandas as pd
import csv
            
def build_solution_csv(df_solution: pd.DataFrame, config: dict) -> str:
    """
    Create a CSV that contains first the configuration (Parametro,Valor)
    and then the solution table. Returns the CSV content as a string.
    """
    buf = io.StringIO()
    buf.write("Parametro,Valor\n")
    for k, v in config.items():
        buf.write(f"{k},{v}\n")
    buf.write("\n")
    df_solution.to_csv(buf, index=False)
    return buf.getvalue()

def build_history_csv(df_history: pd.DataFrame) -> str:
    """Export history DataFrame to CSV and return as string."""
    buf = io.StringIO()
    df_history.to_csv(buf, index=False)
    return buf.getvalue()

def make_filenames(prefix: str = "export") -> tuple:
    """Generate filenames with timestamp for solution and history."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename_sol = f"{prefix}_solucion_config_{ts}.csv"
    filename_hist = f"{prefix}_historial_{ts}.csv"
    return filename_sol, filename_hist

def prepare_exports(df_solution: pd.DataFrame, df_history: pd.DataFrame, config: dict, prefix: str = "export") -> dict:
    """
    Build CSVs and return a dict:
    {
      "csv_sol": <str>,
      "csv_hist": <str>,
      "filename_sol": <str>,
      "filename_hist": <str>
    }
    """
    csv_sol = build_solution_csv(df_solution, config)
    csv_hist = build_history_csv(df_history)
    filename_sol, filename_hist = make_filenames(prefix)
    return {
        "csv_sol": csv_sol,
        "csv_hist": csv_hist,
        "filename_sol": filename_sol,
        "filename_hist": filename_hist
    }
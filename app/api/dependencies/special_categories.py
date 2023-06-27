import os

from fastapi import Depends, Request
from .auth import get_current_user
from app.services.formulas import plots


def get_plot_path(request: Request,
                  user=Depends(get_current_user)):
    """Yield plot image path and remove file aftes"""
    data = request.form()
    functions = []
    for i in range(1, 10):
        function = data.get(f"function{i}")
        if function is not None:
            functions.append(function)

    xmin = data.get("xmin")
    xmax = data.get("xmax")
    ymin = data.get("ymin")
    ymax = data.get("ymax")

    plot = plots.Plot(functions=functions, xlim=(xmin, xmax), ylim=(ymin, ymax))
    plot_path = f"files/plots/{user.id}.png"
    plot.save_plot(path=plot_path)
    yield plot_path
    os.remove(plot_path)

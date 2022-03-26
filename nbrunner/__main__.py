import asyncio
from nbrunner.notebook import JupyterNotebook

async def start():
    nb = JupyterNotebook("Untitled.ipynb")
    await nb.open()
    await nb.run_all_cells()
    await nb.close()

if __name__ == "__main__":
    asyncio.run(start())
import json

from engine3d.mesh import Mesh

def load_mesh_on_file(file: str):
    with open(file=f"{str(file)}", mode="r") as file:
        mesh = json.load(fp=file)
        mesh = Mesh(vertices=mesh["vertices"], faces=mesh["faces"])

    return mesh

def draw_compas_mesh(mesh, color='white', size=1.0):
    """
    Renders a compas mesh on a 3D canvas with ipyvolume.

    Parameters
    ----------
    mesh : :class: compas.datastructures.Mesh
        the mesh to be shown in 3D

    Returns
    -------
    an instance of ipyvolume.widgets.Mesh
    """
    import ipyvolume as ipv

    # extract lists of vertices and faces
    vertices, faces = mesh.to_vertices_and_faces()

    # extract x, y and z values into separate lists
    x = [v[0] for v in vertices]
    y = [v[1] for v in vertices]
    z = [v[2] for v in vertices]

    # triangulate n-gons
    triangles_only = []
    for f in faces:
        if len(f) == 3:
            triangles_only.append(f)
        else:
            for i in range(len(f) - 2):
                triangles_only.append([f[0], f[i+1], f[i+2]])

    # create the ipyvolume plot
    ipv.figure(width=800, height=450)
    viewermesh = ipv.plot_trisurf(x, y, z, triangles_only, color=color)
    ipv.xyzlim(size)
    ipv.style.use('minimal')
    ipv.show()

    return viewermesh

def export_obj_by_attribute(filepath, mesh, attribute):
    """
    Exports a compas mesh to an *.obj file grouping the faces by attribute.

    Parameters
    ----------
    filepath: String
        The path and filename for the export.
    mesh: :class: compas.datastructures.Mesh
        The mesh to be exported.
    attribute: String
        The name of the faces' attribute to group by.
    """
    # if none of the faces has the attribute, export normally
    if not any(mesh.get_faces_attribute(mesh.faces(), attribute)):
        mesh.to_obj(filepath)
        return

    # possible check for faces without attribute:
    # if None in mesh.get_faces_attribute(mesh.faces(), attribute)
    # robust alternative: convert to string > None becomes 'None' group
    fkeys = list(mesh.faces())
    fkeys.sort(key=lambda x: str(mesh.get_face_attribute(x, attribute)))

    key_index = mesh.key_index()
    current_group = 'na'
    with open(filepath, 'w+') as fh:
        for key, attr in mesh.vertices(True):
            fh.write('v {0[x]:.3f} {0[y]:.3f} {0[z]:.3f}\n'.format(attr))
        for fkey in fkeys:
            fa = mesh.get_face_attribute(fkey, attribute)
            if fa != current_group:
                fh.write("g " + str(fa) + "\n")
                current_group = fa

            vertices = mesh.face_vertices(fkey)
            vertices = [key_index[key] + 1 for key in vertices]
            fh.write(' '.join(['f'] + [str(index) for index in vertices]) + '\n')

def draw_compas_mesh(mesh, color='white'):
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
    ipv.style.use('minimal')
    ipv.show()
    
    return viewermesh
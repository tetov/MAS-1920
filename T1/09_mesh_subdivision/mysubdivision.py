from compas.geometry import Vector

def mesh_subdivide_pyramid(mesh, k=1, height=1.0):
    """
    Subdivide a mesh using insertion of a vertex at centroid + height * face normal.

    Parameters
    ----------
    mesh : Mesh
        The mesh object that will be subdivided.
    k : int
        Optional. The number of levels of subdivision. Default is ``1``.
    height : float
        The distance of the new vertex to the face.

    Returns
    -------
    Mesh
        A new subdivided mesh.
    """
    subd = mesh.copy()
    for fkey in mesh.faces():
        centroid = mesh.face_centroid(fkey)
        centroid_vector = Vector(*centroid)
        normal = mesh.face_normal(fkey)
        normal_vector = Vector(*normal)
        new_vertex = centroid_vector + normal_vector * height
        subd.insert_vertex(fkey, xyz=new_vertex)

    return subd

def mesh_subdivide_tapered(mesh, k=1, height=1.0, ratio=0.5):
    """
    TODO
    """
    subd = mesh.copy()
    for fkey in mesh.faces():
        centroid = mesh.face_centroid(fkey)
        centroid_vector = Vector(*centroid)
        normal = mesh.face_normal(fkey)
        normal_vector = Vector(*normal)
        normal_vector *= height

        face_verts = mesh.face_vertices(fkey)
        new_verts = []
        for v in face_verts:
            v_coords = mesh.vertex_coordinates(v)
            v_vector = Vector(*v_coords)
            vert_to_cent = centroid_vector - v_vector
            vert_to_cent *= ratio
            new_vertex = v_vector + vert_to_cent + normal_vector
            x, y, z = new_vertex
            new_verts.append(subd.add_vertex(x=x, y=y, z=z))

        for i,v in enumerate(face_verts):
            next_v = face_verts[(i+1) % len(face_verts)]
            new_v = new_verts[i]
            next_new_v = new_verts[(i+1) % len(face_verts)]
            new_face_key = subd.add_face([v, next_v, next_new_v, new_v])

        top_face_key = subd.add_face(new_verts)
        del subd.face[fkey]
    return subd

def pyramid_face(mesh, fkey, height=0.0):
    centroid = mesh.face_centroid(fkey)
    centroid_vector = Vector(*centroid)
    normal = mesh.face_normal(fkey)
    normal_vector = Vector(*normal)
    new_vertex = centroid_vector + normal_vector * height
    new_keys = mesh.insert_vertex(fkey, xyz=new_vertex, return_fkeys=True)[1]
    return new_keys

def taper_face(mesh, fkey, height=0.0, ratio=0.5, keep_original=False):
    centroid = mesh.face_centroid(fkey)
    centroid_vector = Vector(*centroid)
    normal = mesh.face_normal(fkey)
    normal_vector = Vector(*normal)
    normal_vector *= height

    face_verts = mesh.face_vertices(fkey)
    new_verts = []
    for v in face_verts:
        v_coords = mesh.vertex_coordinates(v)
        v_vector = Vector(*v_coords)
        vert_to_cent = centroid_vector - v_vector
        vert_to_cent *= ratio
        new_vertex = v_vector + vert_to_cent + normal_vector
        x, y, z = new_vertex
        new_verts.append(mesh.add_vertex(x=x, y=y, z=z))

    new_keys = []
    for i,v in enumerate(face_verts):
        next_v = face_verts[(i+1) % len(face_verts)]
        new_v = new_verts[i]
        next_new_v = new_verts[(i+1) % len(face_verts)]
        new_face_key = mesh.add_face([v, next_v, next_new_v, new_v])
        new_keys.append(new_face_key)

    top_face_key = mesh.add_face(new_verts)
    new_keys.append(top_face_key)
    if keep_original==False:
        del mesh.face[fkey]
    return new_keys

def segment_face(mesh, fkey, num=2, start_index = 0):
    f_verts = mesh.face_vertices(fkey)
    if len(f_verts)!=4:
        return fkey

    start_index = start_index % 4

    vc1 = mesh.vertex_coordinates(f_verts[start_index])
    ve1 = mesh.edge_vector(f_verts[start_index], f_verts[(start_index+1)%4])
    vc2 = mesh.vertex_coordinates(f_verts[(start_index+3)%4])
    ve2 = mesh.edge_vector(f_verts[(start_index+2)%4], f_verts[(start_index+3)%4])

    new_verts = []
    for i in range(1,num):
        x1 = vc1[0] + i * ve1[0]/num
        y1 = vc1[1] + i * ve1[1]/num
        z1 = vc1[2] + i * ve1[2]/num
        vn1 = mesh.add_vertex(x=x1, y=y1, z=z1)
        x2 = vc2[0] - i * ve2[0]/num
        y2 = vc2[1] - i * ve2[1]/num
        z2 = vc2[2] - i * ve2[2]/num
        vn2 = mesh.add_vertex(x=x2, y=y2, z=z2)
        new_verts.append((vn1,vn2))


    new_keys = []
    f = mesh.add_face([f_verts[start_index], new_verts[0][0], new_verts[0][1], f_verts[(start_index+3)%4]])
    new_keys.append(f)

    for i in range(num-2):
        f = mesh.add_face([new_verts[i][0], new_verts[i+1][0], new_verts[i+1][1], new_verts[i][1]])
        new_keys.append(f)

    f = mesh.add_face([new_verts[-1][0], f_verts[(start_index+1)%4], f_verts[(start_index+2)%4], new_verts[-1][1]])
    new_keys.append(f)

    del mesh.face[fkey]
    return new_keys

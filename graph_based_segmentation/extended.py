from main import *
from graph import *
import numpy as np

"""
    its very raw code and takes about 10 minutes for 30 iterations
"""
IMAGE_NAME = "example.jpeg"
image_array, image_height, image_width = load_image(IMAGE_NAME)
image_mask = np.zeros(image_array.shape, dtype=float, order='C')

print ("image_height : %d,image_width : %d" % (image_height, image_width))

# intilaizing graph
G = initilaize_graph(image_height * image_width)

# making numpy range
matrix = np.reshape(np.arange(image_height * image_width), [image_height, image_width])
print ("Matrix shape ", matrix.shape)

# get graph
G = get_graph(G, image_array, image_height, image_width)

# get minimum spanning tree for given graph
T = get_m_s_t(G)
# print(sorted(T.edges(data=True)))

# iterate with various threhold to see the change in segmentation with each threshold
# initializing zero matrix
zero_matrix = np.zeros((image_height, image_width))

each_threshold = 27
print ("Current threshold : ", each_threshold)
for each_edge in sorted(T.edges(data=True)):
    try:

        lattice_1_ind, lattice_2_ind, weight = each_edge
        lattice_1 = get_lattice(lattice_1_ind, image_height, image_width)
        lattice_2 = get_lattice(lattice_2_ind, image_height, image_width)
        lattice_1_RBG  = getRGBForPixel(image_array,lattice_1[0], lattice_1[1])
        weight_dict_ = eval(str(weight))
        if float(weight_dict_['weight']) < each_threshold:
            setRGBforPixel(image_mask,lattice_1[0], lattice_1[1],lattice_1_RBG)
            setRGBforPixel(image_mask, lattice_2[0], lattice_2[1], lattice_1_RBG)
    except:
        ""
    # saving image
plt.imshow(image_mask)
plt.show()
# plt.imsave("rabbit_segmented_" + str(each_threshold) + ".jpg", image_mask, cmap='gray')

from graph import *
from scipy.misc import toimage
import matplotlib.pyplot as plt
import traceback

def get_pixel_number(current_row, current_col, image_height, image_width):
    """
    print(get_pixel_number(4,5,6,10)
    :param current_row:
    :param current_col:
    :param image_height:
    :param image_width:
    :return:
    """
    return ((current_row) * image_width) + current_col




def get_pixel_right(current_row, current_col, image_height, image_width):
    """
    give location of pixel right to current pixel
    :param current_row:
    :param current_col:
    :return:
    """
    pixel_right = [current_row, current_col + 1]
    pixel_right_loc = get_pixel_number(pixel_right[0], pixel_right[1], image_height, image_width)
    return pixel_right,pixel_right_loc,

def get_pixel_bottom(current_row, current_col, image_height, image_width):
    """
    give location of pixel bottom to current pixel
    :param current_row:
    :param current_col:
    :return:
    """
    pixel_bottom = [current_row + 1, current_col]
    pixel_bottom_loc = get_pixel_number(pixel_bottom[0], pixel_bottom[1], image_height, image_width)
    return pixel_bottom, pixel_bottom_loc

def get_pixel_diagonal(current_row, current_col, image_height, image_width):
    """
    give location of pixel diagonally right bottom to current pixel
    :param current_row:
    :param current_col:
    :return:
    """
    pixel_diagonal = [current_row + 1, current_col + 1]
    pixel_diagonal_loc = get_pixel_number(pixel_diagonal[0], pixel_diagonal[1], image_height, image_width)
    return pixel_diagonal,pixel_diagonal_loc

def update_graph(G, from_, to_, weight):
    """
    to update given graph, instead to insert new edges with weights
    :param G: Given graph
    :param from_:  from given vertices
    :param to_:   to given vertices
    :param weight: weight of the edge
    :return:
    """
    G.add_edge(from_, to_, weight=weight)
    return G

def get_m_s_t(G):
    """
    getting minimum spanning tree from given graph
    :param G:
    :return:
    """
    return nx.minimum_spanning_tree(G)

def get_graph(G, image_array, image_height, image_width):
    """
    this function provides weight of uni-directed graph for given image.
   :param image_array:
   :param image_height:
   :param image_width:
   :return:
    """
    for height_loc in range(0,image_height):
        for width_loc in range(0,image_width):
            current_pixel_number = get_pixel_number(height_loc, width_loc, image_height, image_width)
            RBG_current = getRGBForPixel(image_array, height_loc, width_loc)
            try:
                # calculating weight w.r.t. neighbours pixel value
                pixel_right, pixel_right_loc = get_pixel_right(height_loc, width_loc, image_height, image_width)
                pixel_bottom, pixel_bottom_loc = get_pixel_bottom(height_loc, width_loc, image_height, image_width)
                pixel_diagonal, pixel_diagonal_loc = get_pixel_bottom(height_loc, width_loc, image_height, image_width)
                # getting pixel number of neighbours
                pixel_right_loc = get_pixel_number(pixel_right[0], pixel_right[1], image_height, image_width)
                pixel_bottom_loc = get_pixel_number(pixel_bottom[0], pixel_bottom[1], image_height, image_width)
                pixel_diagonal_loc = get_pixel_number(pixel_diagonal[0], pixel_diagonal[1], image_height, image_width)
                # getting RBG value
                pixel_right_RGB = getRGBForPixel(image_array, pixel_right[0], pixel_right[1])
                pixel_bottom_RBG = getRGBForPixel(image_array, pixel_bottom[0], pixel_bottom[1])
                pixel_diagonal_RBG = getRGBForPixel(image_array, pixel_diagonal[0], pixel_diagonal[1])
                # updating graph
                G = update_graph(G, current_pixel_number, pixel_right_loc, find_distance(RBG_current, pixel_right_RGB))
                G = update_graph(G, current_pixel_number, pixel_bottom_loc, find_distance(RBG_current, pixel_bottom_RBG))
                G = update_graph(G, current_pixel_number, pixel_diagonal_loc, find_distance(RBG_current, pixel_diagonal_RBG))
            except:# when in last column when width_loc = image_width
                if( width_loc == image_width): #cant move further right
                    pixel_bottom, pixel_bottom_loc = get_pixel_bottom(height_loc, width_loc)
                    pixel_bottom_loc = get_pixel_number(pixel_bottom[0], pixel_bottom[1], image_height, image_width)
                    pixel_bottom_RBG = getRGBForPixel(image_array, pixel_bottom[0], pixel_bottom[1])
                    G = update_graph(G, current_pixel_number, pixel_bottom_loc,
                                     find_distance(RBG_current, pixel_bottom_RBG))
                if( height_loc == image_height): #cant move further down
                    pixel_right, pixel_right_loc = get_pixel_right(height_loc, width_loc)
                    pixel_right_loc = get_pixel_number(pixel_right[0], pixel_right[1], image_height, image_width)
                    pixel_right_RGB = getRGBForPixel(image_array, pixel_right[0], pixel_right[1])
                    G = update_graph(G, current_pixel_number, pixel_right_loc, find_distance(RBG_current, pixel_right_RGB))
    return G

def main (IMAGE_NAME):

    """
    its very raw code and takes about 10 minutes for 30 iterations
    """
    image_array, image_height, image_width = load_image(IMAGE_NAME)
    print ("image_height : %d,image_width : %d" % (image_height, image_width))

    # intilaizing graph
    G = initilaize_graph(image_height * image_width)

    # making numpy range
    matrix = np.reshape(np.arange(image_height * image_width), [image_height, image_width])
    print ("Matrix shape ", matrix.shape)

    #get graph
    G = get_graph(G,image_array, image_height, image_width)
    # get minimum spanning tree for given graph
    T = get_m_s_t(G)

    print(sorted(T.edges(data=True)))


    # iterate with various threhold to see the change in segmentation with each threshold
    for each_threshold in range(0,30,3):
        # initializing zero matrix
        zero_matrix = np.zeros((image_height, image_width))

        print ("Current threshold : ", each_threshold)
        for each_edge in sorted(T.edges(data=True)) :
            try:
                lattice_1_ind, lattice_2_ind , weight = each_edge
                lattice_1 = get_lattice(lattice_1_ind,image_height, image_width)
                lattice_2 = get_lattice(lattice_2_ind, image_height, image_width)
                weight_dict_ = eval(str(weight))
                if float(weight_dict_['weight']) > each_threshold:
                    zero_matrix[lattice_1[0],lattice_1[1]] = 255
                    zero_matrix[lattice_2[0], lattice_2[1]] = 255
            except:
                ""
            # saving image
            plt.imsave("rabbit_background_"+str(each_threshold)+".jpg",zero_matrix,cmap='gray')




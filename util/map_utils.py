import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.patches as patches
import math
from pathlib import Path

# Get the directory of the current module/scrip
dir_path = Path(__file__).parent


def plot_probe_with_electrode_ids(label_ids=None):
    face_color = "green"
    edge_color = [0.3, 0.3, 0.3]
    contact_color = "orange"
    contact_size = 80
    fontsize = 7
    channel_map_df = pd.read_csv(dir_path / 'channel_map.csv')

    # Replace NaN values in 'SG ch#' with a placeholder
    # and convert the rest to integers
    channel_map_df['SG ch#'] = channel_map_df['SG ch#'].\
        where(channel_map_df['SG ch#'].notna(), 'NaN').astype(
            str).str.split('.').str[0]
    fig, ax = plt.subplots(figsize=(6, 8))
    x_triangle = [-40, 0, 40, 40, -40]
    y_triangle = [0, -100, 0, 2100, 2100]
    plt.fill(x_triangle, y_triangle, color=face_color, alpha=0.3)
    ax.scatter(channel_map_df['X, um'], channel_map_df['Y, um'], contact_size,
               color=contact_color, edgecolors=edge_color, alpha=0.7, lw=0.5)
    # Add electrode id label to the left of each point
    if label_ids is None:
        for i, txt in enumerate(channel_map_df['Pad #']):
            ax.annotate(txt, (channel_map_df['X, um'].iloc[i], channel_map_df['Y, um'].iloc[i]),
                        fontsize=fontsize, ha='center', va='center', xytext=(0, -1), textcoords='offset points')
    else:
        for i, txt in enumerate(label_ids):
            ax.annotate(txt, (channel_map_df['X, um'].iloc[i], channel_map_df['Y, um'].iloc[i]),
                        fontsize=fontsize, ha='center', va='center', xytext=(0, -1), textcoords='offset points')
    # for i, txt in enumerate(channel_map_df['SG ch#']):
    #     ax.annotate(txt, (channel_map_df['X, um'].iloc[i], channel_map_df['Y, um'].iloc[i]),
    #                 fontsize=6, ha='right', va='center', xytext=(17, 0), textcoords='offset points')
    plt.plot([-40, -40], [0, 3000], '-', color=edge_color, alpha=0.3, lw=0.5)
    plt.plot([40, 40], [0, 3000], '-', color=edge_color, alpha=0.3, lw=0.5)
    x1 = [-40, 0]
    y1 = [0, -100]
    x2 = [0, 40]
    y2 = [-100, 0]
    plt.plot(x1, y1, '-', color=edge_color, alpha=0.3, lw=0.5)
    plt.plot(x2, y2, '-', color=edge_color, alpha=0.3, lw=0.5)
    ax.set_xlabel('X (um)')
    ax.set_ylabel('Y (um)')
    plt.tight_layout()
    plt.xlim([-100, 100])
    plt.ylim([-150, 2100])
    ax.set_aspect(0.4)
    plt.show()


def map_electrode_ids_to_flex_cable_ids():
    # use SG ch# in spreadsheet to map pad # or elec id to flex cable id
    df = pd.read_csv(dir_path / 'old_flex_cable_hardware_ids.csv')
    old_j3_ids = df['j3'].tolist()
    old_j4_ids = df['j4'].tolist()
    new_j3_ids = np.arange(72, 143)  # right
    new_j4_ids = np.arange(1, 72)
    old_flex_ids = np.concatenate([old_j4_ids, old_j3_ids])  # from 1 to 142
    new_flex_ids = np.concatenate([new_j4_ids, new_j3_ids])  # from 1 to 142
    channel_map_df = pd.read_csv(dir_path / 'channel_map.csv')
    channel_map_df['SG ch#'].replace('', np.nan, inplace=True)
    sg_chs = [int(value) if not np.isnan(value) else -
              1 for value in channel_map_df['SG ch#']]
    electrode_IDs = np.arange(1, 130)

    electrode_to_flex = {}
    for elec_id in electrode_IDs:
        sg_ch = sg_chs[elec_id-1]
        if sg_ch == -1:
            continue
        idx = np.where(old_flex_ids == sg_ch)[0][0]
        new_id = new_flex_ids[idx]
        electrode_to_flex[elec_id] = new_id

    electrode_to_sg_chs = {}
    for elec_id in electrode_IDs:
        sg_ch = sg_chs[elec_id-1]
        electrode_to_sg_chs[elec_id] = sg_ch

    return electrode_to_flex, electrode_to_sg_chs


def sort_electrode_ids_by_flex_cable_pos(electrode_to_flex):
    flex_to_electrode = {value: key for key,
                         value in electrode_to_flex.items()}
    # Top 7 pads for each side don't map to electrode IDs
    not_connected = [1, 2, 3, 4, 5, 6, 7, 72, 73, 74, 75, 76, 77, 78]
    # Corresponding values for flex_to_electrode dict should be nan
    for key in not_connected:
        flex_to_electrode[key] = np.nan
    sorted_dict = {
        key: flex_to_electrode[key] for key in sorted(flex_to_electrode)}
    sorted_electrode_ids = sorted_dict.values()
    return sorted_electrode_ids


def get_old_hardware_flex_cable_ids():
    df = pd.read_csv(dir_path / 'old_flex_cable_hardware_ids.csv')
    old_j3_ids = df['j3'].tolist()
    old_j4_ids = df['j4'].tolist()
    old_flex_ids = np.concatenate([old_j4_ids, old_j3_ids])  # from 1 to 142
    old_flex_ids = [int(x) if not np.isnan(
        x) else np.nan for x in old_flex_ids]
    return old_flex_ids


def generate_flex_positions(flex_IDs, side, num_rows=71):
    positions = []
    for id in flex_IDs:
        if side == 'left':
            col = 1 if (id - flex_IDs[0]) % 2 == 1 else 0
        else:
            col = 0 if (id - flex_IDs[0]) % 2 == 1 else 1
        positions.append((col, num_rows - (id - flex_IDs[0])))
    return positions


def create_flex_cable_ids():
    # assume 70 pads per wing
    # use 1-indexing
    left_flex_IDs = np.arange(1, 72)
    right_flex_IDs = np.arange(72, 143)
    left_flex_pos = generate_flex_positions(left_flex_IDs, side='left')
    right_flex_pos = generate_flex_positions(right_flex_IDs, side='right')

    return left_flex_IDs, right_flex_IDs, left_flex_pos, right_flex_pos


def plot_flex_cable_ids(label_ids=None, title="Flex Cable Positional IDs"):
    left_flex_IDs, right_flex_IDs, left_flex_pos, right_flex_pos = create_flex_cable_ids()
    left_x_coords = [coord[0] for coord in left_flex_pos]
    left_y_coords = [coord[1] for coord in left_flex_pos]
    right_x_coords = [coord[0] for coord in right_flex_pos]
    right_y_coords = [coord[1] for coord in right_flex_pos]

    x_rect_left = -0.5
    y_rect_left = -1
    x_rect_right = 2.65
    y_rect_right = -1
    width = 2
    height = 74
    rect_color = 'lightgray'
    fig, ax = plt.subplots(figsize=(6, 8))

    ax.add_patch(patches.Rectangle(
        (x_rect_left, y_rect_left), width, height, color=rect_color, fill=True))
    ax.text(x_rect_left + width/2, y_rect_left -
            1, 'J4', ha='center', va='top')
    ax.scatter(left_x_coords, left_y_coords)

    ax.add_patch(patches.Rectangle(
        (x_rect_right, y_rect_right), width, height, color=rect_color, fill=True))
    ax.text(x_rect_right + width/2, y_rect_right -
            1, 'J3', ha='center', va='top')
    ax.scatter(np.array(right_x_coords) + 3, right_y_coords, color='C0')

    if label_ids is None:
        label_ids = np.concatenate([left_flex_IDs, right_flex_IDs])
    # Annotate using label_ids
    for i, label in enumerate(label_ids):
        if i < len(left_flex_IDs):  # This means it's a left ID
            ax.annotate(label, (left_x_coords[i], left_y_coords[i]),
                        fontsize=8, ha='right', va='center', xytext=(20, 0), textcoords='offset points')
        else:  # This means it's a right ID
            idx = i - len(left_flex_IDs)
            ax.annotate(label, (right_x_coords[idx] + 3, right_y_coords[idx]),
                        fontsize=8, ha='right', va='center', xytext=(20, 0), textcoords='offset points')
    plt.xlim([-1, 5])
    plt.ylim([-1, 75])
    plt.title(title)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis('off')
    plt.title(title)
    plt.show()


def generate_ZIF_positions(zif_ids, z_index, num_rows=71):
    positions = []
    for id in zif_ids:
        if z_index == 2:
            col = 1 if id % 2 == 1 else 0
            positions.append((col, id))
        else:
            col = 0 if id % 2 == 1 else 1
            positions.append((col,  num_rows - (id - zif_ids[0])))
    return positions


def create_ZIF_ids():
    left_zif_ids = np.concatenate(
        [np.arange(71, 0, -2), np.arange(70, 1, -2)])
    left_zif_ids = sorted(left_zif_ids, reverse=True)
    right_zif_ids = np.concatenate(
        [np.arange(1, 72, 2), np.arange(2, 71, 2)])
    right_zif_ids = sorted(right_zif_ids)
    left_zif_pos = generate_ZIF_positions(left_zif_ids, 2)
    right_zif_pos = generate_ZIF_positions(right_zif_ids, 1)
    L_str_ids = ['L' + str(left_zif_id) for left_zif_id in left_zif_ids]
    R_str_ids = ['R' + str(right_zif_id) for right_zif_id in right_zif_ids]
    LR_str_ids = L_str_ids + R_str_ids
    return left_zif_ids, right_zif_ids, left_zif_pos, right_zif_pos, LR_str_ids


def map_flex_cable_to_ZIF():
    # j4 -> zif1 or left zif
    # j3 -> zif2 or right zif
    left_zif_ids, right_zif_ids, _, _, LR_str_ids = create_ZIF_ids()
    left_flex_ids, right_flex_ids, _, _ = create_flex_cable_ids()
    left_flex_to_ZIF1 = {}
    right_flex_to_ZIF2 = {}
    for i, id in enumerate(left_flex_ids):
        left_flex_to_ZIF1[id] = 'L' + str(left_zif_ids[i])
    for i, id in enumerate(right_flex_ids):
        right_flex_to_ZIF2[id] = 'R' + str(right_zif_ids[i])
    flex_to_ZIF = left_flex_to_ZIF1 | right_flex_to_ZIF2
    return left_flex_to_ZIF1, right_flex_to_ZIF2, flex_to_ZIF


def sort_flex_ids_by_ZIF_pos():
    left_zif_ids, right_zif_ids, _, _, _ = create_ZIF_ids()
    left_flex_ids = left_zif_ids[::-1]
    right_flex_ids = list(np.array(right_zif_ids) + 71)
    sorted_flex_ids = left_flex_ids + right_flex_ids
    return sorted_flex_ids


def sort_electrode_ids_by_ZIF_pos(electrode_to_ZIF_dict):
    ZIF_to_electrode = {value: key for key,
                        value in electrode_to_ZIF_dict.items()}
    # Top 7 pads for each side don't map to electrode IDs
    _, _, _, _, desired_order = create_ZIF_ids()
    not_connected = ['L71', 'L70', 'L69', 'L68', 'L67', 'L66',
                     'L65', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7']
    for key in not_connected:
        ZIF_to_electrode[key] = np.nan
    # Create a new dictionary with keys in the desired order
    sorted_dict = {key: ZIF_to_electrode[key]
                   for key in desired_order if key in ZIF_to_electrode}
    sorted_electrode_ids = sorted_dict.values()
    return sorted_electrode_ids


def plot_ZIF_ids(label_ids=None, title="ZIF Connectors Positional IDs"):
    left_zif_ids, right_zif_ids, left_zif_pos, right_zif_pos, LR_str_ids = create_ZIF_ids()

    right_x_offset = 3
    left_x_coords = [coord[0] for coord in left_zif_pos]
    left_y_coords = [coord[1] for coord in left_zif_pos]
    right_x_coords = [coord[0] + right_x_offset for coord in right_zif_pos]
    right_y_coords = [coord[1] for coord in right_zif_pos]

    x_zif_left = -0.5
    x_zif_left = min(left_x_coords) - 0.3
    y_zif_left = -1
    x_zif_right = min(right_x_coords) - 0.3
    y_zif_right = -1
    width = 2
    height = 74
    rect_color = 'lightgray'

    fig, ax = plt.subplots(figsize=(6, 8))
    ax.add_patch(patches.Rectangle(
        (x_zif_left, y_zif_left), width, height, color=rect_color, fill=True))
    ax.text(x_zif_left + width/2, y_zif_left -
            1, 'Z1', ha='center', va='top')
    ax.scatter(left_x_coords, left_y_coords)

    ax.add_patch(patches.Rectangle(
        (x_zif_right, y_zif_right), width, height, color=rect_color, fill=True))
    ax.text(x_zif_right + width/2, y_zif_right -
            1, 'Z2', ha='center', va='top')
    ax.scatter(right_x_coords, right_y_coords, color='C0')

    # If label_ids is not provided, fall back to enumeration of left_IDs and right_IDs
    if label_ids is None:
        label_ids = np.concatenate([left_zif_ids, right_zif_ids])
    # Annotate using label_ids
    for i, label in enumerate(label_ids):
        if i < len(left_zif_ids):  # This means it's a left ID
            ax.annotate(label, (left_x_coords[i], left_y_coords[i]),
                        fontsize=8, ha='left', va='center', xytext=(8, 0), textcoords='offset points')
        else:  # This means it's a right ID
            idx = i - len(left_zif_ids)
            ax.annotate(label, (right_x_coords[idx], right_y_coords[idx]),
                        fontsize=8, ha='left', va='center', xytext=(8, 0), textcoords='offset points')
    plt.xlim([-1, 5])
    plt.ylim([-1, 75])
    plt.title(title)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis('off')
    plt.show()


def create_samtec_ids():
    samtec_ids = []
    samtec_pos = []
    for mt_index in range(4):
        ref1 = 'ref1_' + str(mt_index)
        ref2 = 'ref2_' + str(mt_index)
        gnd1 = 'gnd1_' + str(mt_index)
        gnd2 = 'gnd2_' + str(mt_index)

        samtec_ids_i = list(
            np.arange(mt_index * 32 + 1, (mt_index + 1) * 32 + 1))
        samtec_ids_i.extend([ref1, ref2, gnd1, gnd2])

        # Directly extend the main samtec_ids and samtec_pos lists
        samtec_ids.extend(samtec_ids_i)
        samtec_pos.extend(generate_samtec_positions(samtec_ids_i, mt_index))
    return samtec_ids, samtec_pos


def generate_samtec_positions(samtec_ids, mt_index, num_rows=18):
    positions = []
    for id in samtec_ids:
        if type(id) != str:
            if id < samtec_ids[16]:
                col = 0
                row = num_rows - (id - mt_index * 32)
            else:
                col = 1
                if mt_index == 0:
                    row = id - 15
                else:
                    row = id - (mt_index * 32 + 15)
        else:  # if ref or gnd
            if 'ref1' in id:
                col = 0
                row = 1
            elif 'ref2' in id:
                col = 1
                row = 0
            elif 'gnd1' in id:
                col = 1
                row = 1
            elif 'gnd2' in id:
                col = 0
                row = 0
        positions.append((col,  row))
    return positions


def map_ZIF_to_samtec():
    zif_to_samtec_df = pd.read_csv(
        dir_path / 'ZIF_connector_to_Samtec_map.csv')
    left_zif_ids = zif_to_samtec_df['ZIF 1']
    right_zif_ids = zif_to_samtec_df['ZIF 2']
    from_left_zif = zif_to_samtec_df['Samtec 1']
    from_right_zif = zif_to_samtec_df['Samtec 2']

    ZIF1_to_samtec = {}
    ZIF2_to_samtec = {}
    for i, id in enumerate(left_zif_ids):
        value = from_left_zif[i]
        ZIF1_to_samtec['L' +
                       str(id)] = int(value) if not np.isnan(value) else value
    for i, id in enumerate(right_zif_ids):
        value = from_right_zif[i]
        ZIF2_to_samtec['R' +
                       str(id)] = int(value) if not np.isnan(value) else value

    ZIF_to_samtec = ZIF1_to_samtec | ZIF2_to_samtec
    return ZIF_to_samtec


def sort_ZIF_ids_by_samtec_pos(ZIF_to_samtec_dict):
    samtec_to_ZIF = {value: key for key,
                     value in ZIF_to_samtec_dict.items()}
    sorted_dict = {
        key: samtec_to_ZIF[key]
        for key in sorted(samtec_to_ZIF)
        if key == key and not math.isnan(float(key))
    }
    sorted_ZIF_ids = list(sorted_dict.values())
    insert_list = ['ref1', 'ref2', 'gnd1', 'gnd2']
    for i in range(1, len(sorted_ZIF_ids)//32 + 1):
        insert_index = 32 * i + 4 * (i - 1)
        sorted_ZIF_ids[insert_index:insert_index] = insert_list
    return sorted_ZIF_ids


def sort_electrode_ids_by_samtec_pos(electrode_to_samtec_dict):
    samtec_to_electrode = {value: key for key,
                           value in electrode_to_samtec_dict.items()}
    sorted_dict = {
        key: samtec_to_electrode[key]
        for key in sorted(samtec_to_electrode)
        if key == key and not math.isnan(float(key))
    }
    sorted_electrode_ids = list(sorted_dict.values())
    insert_list = ['ref1', 'ref2', 'gnd1', 'gnd2']
    for i in range(1, len(sorted_electrode_ids)//32 + 1):
        insert_index = 32 * i + 4 * (i - 1)
        sorted_electrode_ids[insert_index:insert_index] = insert_list
    return sorted_electrode_ids


def plot_samtec_ids(label_ids=None, title="Samtec Connectors Positional IDs"):
    samtec_ids, samtec_pos = create_samtec_ids()
    fig, ax = plt.subplots(figsize=(6, 8))

    width = 4
    height = 19
    rect_color = 'lightgray'

    if label_ids is None:
        label_ids = samtec_ids

    n = len(samtec_ids) // 4  # Number of ids per connector

    for mt_id in range(4):
        start_idx = mt_id * n
        end_idx = (mt_id + 1) * n

        x_coords = [coord[0]*2+mt_id *
                    5 for coord in samtec_pos[start_idx:end_idx]]
        y_coords = [coord[1] for coord in samtec_pos[start_idx:end_idx]]

        ax.add_patch(patches.Rectangle(
            (x_coords[0]-0.5, -1), width, height, color=rect_color, fill=True))
        ax.scatter(x_coords, y_coords, color='C0')
        ax.text(x_coords[0]+width/3, -1.5, str(mt_id+1), ha='center', va='top')

        mt_id_labels = label_ids[start_idx:end_idx]
        if mt_id > 0:
            midpoint = 28
            mt_id_labels = mt_id_labels[:16] + \
                mt_id_labels[16:32][::-1] + mt_id_labels[-4:]
        for i, label in enumerate(mt_id_labels):
            if type(label) == str and ('ref' in label or 'gnd' in label):
                label = label.split('_')[0]
            ax.annotate(label, (x_coords[i], y_coords[i]),
                        fontsize=8, ha='left', va='center', xytext=(5, 0), textcoords='offset points')

    plt.title(title)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis('off')
    plt.show()


def generate_ripple_positions(ripple_ids, fe_index, num_rows=18):
    positions = []
    for id in ripple_ids:
        if type(id) != str:
            col = id % 2
            row = (num_rows - np.ceil(id / 2)) + fe_index * (num_rows - 2)

        else:  # if ref or gnd
            if 'ref1' in id:
                col = 0
                row = 1
            elif 'ref2' in id:
                col = 1
                row = 0
            elif 'gnd1' in id:
                col = 1
                row = 1
            elif 'gnd2' in id:
                col = 0
                row = 0
        positions.append((col,  row))
    return positions


def create_ripple_ids():
    ripple_ids = []
    ripple_pos = []
    for fe_index in range(4):
        ref1, ref2, gnd1, gnd2 = [f'{name}_{fe_index}' for name in
                                  ['ref1', 'ref2', 'gnd1', 'gnd2']]
        ripple_ids_i = list(
            np.arange(fe_index * 32 + 1, (fe_index + 1) * 32 + 1))
        ripple_ids_i.extend([ref1, ref2, gnd1, gnd2])

        # Directly extend the main samtec_ids and samtec_pos lists
        ripple_ids.extend(ripple_ids_i)
        ripple_pos.extend(generate_ripple_positions(ripple_ids_i, fe_index))
    return ripple_ids, ripple_pos


def map_samtec_to_ripple():
    df = pd.read_csv(dir_path / 'Samtec_connector_to_Ripple_map.csv')
    samtec_ids = df['Samtec'].tolist()
    ripple_ids = df['Ripple'].tolist()
    samtec_to_ripple = {samtec_ids[i]: ripple_ids[i]
                        for i in range(len(samtec_ids))}
    return samtec_to_ripple


def sort_samtec_ids_by_ripple_pos(samtec_to_ripple_dict):
    ripple_to_samtec = {value: key for key,
                        value in samtec_to_ripple_dict.items()}
    sorted_dict = {
        key: ripple_to_samtec[key]
        for key in sorted(ripple_to_samtec)
        if key == key and not math.isnan(float(key))
    }
    sorted_samtec_ids = list(sorted_dict.values())
    insert_list = ['ref1', 'ref2', 'gnd1', 'gnd2']
    for i in range(1, len(sorted_samtec_ids)//32 + 1):
        insert_index = 32 * i + 4 * (i - 1)
        sorted_samtec_ids[insert_index:insert_index] = insert_list
    return sorted_samtec_ids


def sort_electrode_ids_by_ripple_pos(electrode_to_ripple_dict):
    ripple_to_electrode = {value: key for key,
                           value in electrode_to_ripple_dict.items()}
    sorted_dict = {
        key: ripple_to_electrode[key]
        for key in sorted(ripple_to_electrode)
        if key == key and not math.isnan(float(key))
    }
    sorted_ripple_ids = list(sorted_dict.values())
    insert_list = ['ref1', 'ref2', 'gnd1', 'gnd2']
    for i in range(1, len(sorted_ripple_ids)//32 + 1):
        insert_index = 32 * i + 4 * (i - 1)
        sorted_ripple_ids[insert_index:insert_index] = insert_list
    return sorted_ripple_ids


def plot_ripple_ids(label_ids=None, title="Ripple FE Positional IDs"):
    ripple_ids, ripple_pos = create_ripple_ids()
    fig, ax = plt.subplots(figsize=(6, 8))

    width = 4
    height = 19
    rect_color = 'lightgray'

    if label_ids is None:
        label_ids = ripple_ids

    n = len(ripple_ids) // 4  # Number of ids per connector

    for fe_id in range(4):
        start_idx = fe_id * n
        end_idx = (fe_id + 1) * n

        x_coords = [coord[0]*2 + fe_id *
                    5 for coord in ripple_pos[start_idx:end_idx]]
        y_coords = [coord[1] for coord in ripple_pos[start_idx:end_idx]]

        ax.add_patch(patches.Rectangle(
            (x_coords[1]-0.5, -1), width, height, color=rect_color, fill=True))
        ax.scatter(x_coords, y_coords, color='C0')
        ax.text(x_coords[1]+width/3, -1.5, str(fe_id+1), ha='center', va='top')

        fe_id_labels = label_ids[start_idx:end_idx]
        # if fe_id > 0:
        #     midpoint = 28
        #     fe_id_labels = fe_id_labels[:16] + \
        #         fe_id_labels[16:32][::-1] + fe_id_labels[-4:]
        for i, label in enumerate(fe_id_labels):
            if type(label) == str and ('ref' in label or 'gnd' in label):
                label = label.split('_')[0]
            ax.annotate(label, (x_coords[i], y_coords[i]),
                        fontsize=8, ha='left', va='center', xytext=(5, 0), textcoords='offset points')

    plt.title(title)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis('off')
    plt.show()

import numpy as np
from qiskit_metal import draw, Dict
from qiskit_metal.qlibrary.qubits.transmon_pocket import TransmonPocket
#from qiskit_metal.qlibrary.core import Qcomponent
from qiskit_metal.qlibrary.core import BaseQubit


class FluxQubit4jj(BaseQubit):  # pylint: disable=invalid-name
    """Flux Qubit with 4 Josephson Junctions."""
    component_metadata = Dict(short_name='Flux4jj',
                              _qgeometry_table_path='True',
                              _qgeometry_table_poly='True',
                              _qgeometry_table_junction='True')
    """Component metadata"""

    default_options = Dict(
        alpha=0.5,
        jj_side='0.25um',
        jj_spacing='0.001mm',
        constriction_width='0.02um',
        branches_spacing='0.003mm',
        inductor_width='0.002mm',
        cpw_length='0.010mm',
        cpw_width = '0.0025mm',
        cpw_gap = '0.004mm',
        pos_x='0um',
        pos_y='0um',
        orientation=0,
        )
    """Default drawing options"""

    def make(self):
        """Define the way the options are turned into QGeometry.

        The make function implements the logic that creates the geometry
        (poly, path, etc.) from the qcomponent.options dictionary of
        parameters, and the adds them to the design, using
        qcomponent.add_qgeometry(...), adding in extra needed
        information, such as layer, subtract, etc.
        """
        self.make_connections()
        self.make_pocket()
        

    def make_pocket(self):
        """Create the component"""
        p = self.parse_options()
        """Parse the options"""

        small_jj_side = p.jj_side * np.sqrt(p.alpha)
        to_constriction_wire_width = p.constriction_width * 4
        constriction_length = p.jj_spacing * 0.8
        to_constriction_wire_length = p.jj_spacing * 0.1 + p.jj_side
        pocket_width =  p.branches_spacing + 8*p.jj_side
        pocket_height = 5*p.jj_spacing + 7*p.jj_side

        

        rect_1_branch_1 = draw.rectangle(
            2*p.jj_side,
            1.5*p.jj_spacing,
            p.pos_x,
            p.pos_y
            )
        
        rect_1_branch_2 = draw.translate(
            rect_1_branch_1,
            p.branches_spacing,
            0
            )
        
        rect_7_branch_1 = draw.translate(
            rect_1_branch_1,
            0,
            -3.5*p.jj_spacing - 2*p.jj_side
        )

        rect_7_branch_2 = draw.translate(
            rect_7_branch_1,
            p.branches_spacing,
            0
        )

        rect_2_branch_2 = draw.rectangle(p.jj_side, 0.5*p.jj_spacing, p.pos_x + p.branches_spacing, p.pos_y - p.jj_spacing)
        rect_2_branch_1 = draw.rectangle(small_jj_side, 0.5*p.jj_spacing, p.pos_x, p.pos_y - p.jj_spacing)
        
        jj1 = draw.LineString([
            (p.pos_x, p.pos_y - 1.25*p.jj_spacing),
            (p.pos_x, p.pos_y - 1.25*p.jj_spacing - small_jj_side)])
        
        jj3 = draw.LineString([
            (p.pos_x + p.branches_spacing, p.pos_y - 1.25*p.jj_spacing),
            (p.pos_x + p.branches_spacing, p.pos_y - 1.25*p.jj_spacing - p.jj_side)])
        
        #CHECK THESE TANSFORMATIONS
        rect_6_branch_2 = draw.translate(rect_2_branch_2, 0, -1.5*p.jj_spacing - 2*p.jj_side)
        rect_6_branch_1 = draw.translate(rect_6_branch_2, -p.branches_spacing, 0)

        rect_3_branch_2 = draw.rectangle(
            2*p.jj_side,
            p.jj_side,
            p.pos_x + p.branches_spacing - 1.5*p.jj_side,
            p.pos_y - p.jj_spacing - 0.25*p.jj_spacing - 0.5*p.jj_side,
            )
        rect_3_branch_1 = draw.rectangle(
            2*p.jj_side,
            small_jj_side,
            p.pos_x - p.jj_side - 0.5*small_jj_side,
            p.pos_y - p.jj_spacing - 0.25*p.jj_spacing - 0.5*small_jj_side,
        )
        rect_5_branch_2 = draw.translate(rect_3_branch_2, 0, -p.jj_spacing - p.jj_side)
        rect_5_branch_1 = draw.translate(rect_5_branch_2, -p.branches_spacing, 0)

        jj4 = draw.translate(
            jj3,
            0,
            -p.jj_spacing - p.jj_side
        )

        jj2 = draw.translate(
            jj4,
            -p.branches_spacing,
            0
        )

        rect_4_branch_2 = draw.rectangle(
            to_constriction_wire_width,
            p.jj_spacing + 2*p.jj_side,
            p.pos_x + p.branches_spacing - 2.5*p.jj_side - 0.5*to_constriction_wire_width,
            p.pos_y - p.jj_spacing - 0.75*p.jj_spacing - p.jj_side,
        )

        to_constriction = draw.rectangle(
            to_constriction_wire_width,
            to_constriction_wire_length,
            p.pos_x - 2*p.jj_side - 0.5*small_jj_side - 0.5*to_constriction_wire_width,
            p.pos_y - p.jj_spacing - 0.25*p.jj_spacing - to_constriction_wire_length/2,
            )
        
        from_constriction = draw.translate(
            to_constriction,
            0,
            -to_constriction_wire_length - constriction_length,
        )

        constriction = draw.rectangle(
            p.constriction_width,
            constriction_length,
            p.pos_x - 2*p.jj_side - 0.5*small_jj_side - 0.5*to_constriction_wire_width,
            p.pos_y - p.jj_spacing - 0.25*p.jj_spacing - to_constriction_wire_length - constriction_length/2,
        )

        rect_0 = draw.rectangle(
            p.branches_spacing + 2*p.jj_side,
            2*p.jj_side,
            p.pos_x + 0.5*p.branches_spacing,
            p.pos_y + 0.75*p.jj_spacing + p.jj_side,
        )

        rect_8 = draw.translate(
            rect_0,
            0,
            -5*p.jj_spacing - 4*p.jj_side
        )

        top_pad = draw.union(
            rect_1_branch_1,
            rect_1_branch_2,
            rect_2_branch_1,
            rect_2_branch_2,
            rect_0,
        )

        down_pad = draw.union(
            rect_6_branch_2,
            rect_6_branch_1,
            rect_7_branch_1,
            rect_7_branch_2,
            rect_8,
        )

        intra_j_spacing_2 = draw.union(
            rect_3_branch_2,
            rect_4_branch_2,
            rect_5_branch_2,
            )

        intra_j_spacing_1 = draw.union(
            to_constriction,
            constriction,
            from_constriction,
            rect_5_branch_1,
            rect_3_branch_1
        )

        pckt = draw.rectangle(
            pocket_width,
            pocket_height,
            p.pos_x + 0.5*p.branches_spacing,
            p.pos_y - pocket_height/2 + p.jj_spacing + p.jj_side,
        )

        polys = [
            jj1,
            jj2,
            jj3,
            jj4,
            top_pad,
            down_pad,
            intra_j_spacing_1,
            intra_j_spacing_2,
            pckt,
        ]

        polys = draw.rotate(polys, p.orientation, origin=(p.pos_x, p.pos_y))

        [
            jj1,
            jj2,
            jj3,
            jj4,
            top_pad,
            down_pad,
            intra_j_spacing_1,
            intra_j_spacing_2,
            pckt,
        ] = polys


        self.add_qgeometry('poly', dict(
            top_pad=top_pad,
            down_pad=down_pad,
            intra_j_spacing_1=intra_j_spacing_1,
            intra_j_spacing_2=intra_j_spacing_2,
        ))
        self.add_qgeometry('poly', dict(
            pckt=pckt
            ),
        subtract=True,
        )
        self.add_qgeometry('junction', dict(
            jj1=jj1, 
        ),
        width = small_jj_side,
        )
        self.add_qgeometry('junction',
            dict(
                jj3=jj3,
                jj2=jj2,
                jj4=jj4
            ),
            width = p.jj_side,
        )

        
        
    def make_connections(self):
        p = self.parse_options()

        #cpw_path = draw.rectangle(
        #    p.cpw_length,
        #    p.cpw_width,
        #    p.pos_x + 0.5*p.branches_spacing,
        #    p.pos_y + 0.75*p.jj_spacing + 2*p.jj_side + p.cpw_width,
        #)

        cpw_path = draw.LineString(
            [
                (p.pos_x + 0.5*p.branches_spacing - p.cpw_length/2, p.pos_y + 0.75*p.jj_spacing + 2*p.jj_side + p.cpw_width/2),
                (p.pos_x + 0.5*p.branches_spacing + p.cpw_length/2, p.pos_y + 0.75*p.jj_spacing + 2*p.jj_side + p.cpw_width/2)
            ]
        )

        cpy = draw.LineString([
                (p.pos_x + 0.5*p.branches_spacing + p.cpw_length/2, p.pos_y + 0.75*p.jj_spacing + 2*p.jj_side + p.cpw_width/2),
                (p.pos_x + 0.5*p.branches_spacing - p.cpw_length/2, p.pos_y + 0.75*p.jj_spacing + 2*p.jj_side + p.cpw_width/2),
            ])

        cpw_path = draw.rotate(cpw_path, p.orientation, origin=(p.pos_x, p.pos_y))
        
        self.add_qgeometry('path', {f'cpw_wire': cpw_path},
                           width=p.cpw_width)
        self.add_qgeometry('path', {f'cpw_wire_sub': cpw_path},
                           width=p.cpw_width + 2*p.cpw_gap,
                           subtract=True) 
        #print(cpw_path.exterior.coords)
        points = np.array(cpw_path.coords)
        #print(points[1:3])
        #points_out = points[[0,3]]
        #print(points_out)
        print(points)

        self.add_pin('cpw_out',
                     #points=points[2:0:-1],
                     points=points[-2:],
                     width=p.cpw_width,
                     input_as_norm=True)
        

        points_out = np.array(cpy.coords)
        
        self.add_pin('cpw_in',
                     points=points_out[-2:],
                     width=p.cpw_width,
                     input_as_norm=True)







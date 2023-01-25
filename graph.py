import copy
import math
from typing import List, Dict, Optional, Tuple
from loader import Loader
#from vertex import Vertex
#from edge import Edge
#from read import Read


class Vertex(object):
    
    
    def __init__(self, sequence: str) -> None:
        """

        Args:
            sequence (str): Chuỗi đánh dấu đỉnh
        """
        
        self.sequence: str = sequence
        self.in_edges: List[Edge] = []
        self.out_edges: List[Edge] = []
    
    
    def __getitem__(self, n: int) -> str:
        """Lấy ký tự thứ n trong chuỗi đại diện cho đỉnh

        Args:
            n (int): Vị trí n mà ký tự cần lấy

        Returns:
            str: Ký tự tại vị trí được chọn
        """
        
        return self.sequence[n]
    
    
    def __len__(self) -> int:
        """Trả về độ dài của chuỗi đại diện cho đỉnh

        Returns:
            int: Độ dài của chuỗi đại diện cho đỉnh
        """
        
        return len(self.sequence)
    
    
    def __str__(self) -> str:
        """Trả vệ nội dung chuỗi đại diện cho đỉnh

        Returns:
            str: Chuỗi đại diện cho đỉnh
        """
        
        return self.sequence
    
    
    def add_out_edge(self, out_vertex, edge) -> None:
        """ Thêm một cạnh đi ra từ đỉnh hiện tại

        Args:
            out_vertex (Vertex): Đỉnh đích của cạnh đi ra từ đỉnh hiện tại
            edge (_type_): Cạnh cần được thêm đi ra từ đỉnh hiện tại
        """    
        
        self.out_edges.append(edge)
        out_vertex.in_edges.append(edge)
        
        
class Edge(object):
    
    
    def __init__(self, in_vertex: Vertex, out_vertex: Vertex, sequence: str) -> None:
        """

        Args:
            in_vertex (Vertex): Đỉnh bắt đầu cạnh hiện tại
            out_vertex (Vertex): Đỉnh kết thúc cạnh hiện tại
            sequence (str): Chuỗi đại diện cho cạnh hiện tại
        """
        
        self.sequence: str = sequence
        self.in_vertex: Vertex = in_vertex
        self.out_vertex: Vertex = out_vertex
        self.reads: List[Read] = []
        self.multiplicities: int = 1
        self.visited: int = 0
        
    
    def __getitem__(self, n: int) -> str:
        """Lấy ký tự thứ n trong chuỗi đại diện cho cạnh

        Args:
            n (int): Vị trí n mà ký tự cần lấy

        Returns:
            str: Ký tự tại vị trí được chọn
        """
        
        return self.sequence[n]
    
    
    def __len__(self) -> int:
        """Trả về độ dài của chuỗi đại diện cho cạnh

        Returns:
            int: Độ dài của chuỗi đại diện cho cạnh
        """
        return len(self.sequence)
    
    
    def __str__(self) -> str:
        """Trả vệ nội dung chuỗi đại diện cho đỉnh

        Returns:
            str: Chuỗi đại diện cho đỉnh
        """
        return self.sequence
    
    
class Read(object):
    
    def __init__(self, sequence: str, read_id: int) -> None:
        """

        Args:
            sequence (str): Chuỗi đại diện cho read
            read_id (int): id của read
        """
        self.sequence: str = sequence
        self.read_id: int = read_id
        self.edges: List[Edge] = []
        
        
    def __getitem__(self, n: int) -> Edge:
        """Lấy cạnh thứ n trong danh sách các cạnh của read hiện tại

        Args:
            n (int): Vị trí của cạnh cần được lấy

        Returns:
            Edge: Cạnh ở vị trí cần được lấy
        """
        return self.edges[n]
    
    
    def change_x(self, x: Edge, z: Edge) -> bool:
        """Thay đổi cạnh cuối cùng trong tập các cạnh thành cạnh mới z nếu x là cạnh cuối

        Args:
            x (Edge): Cạnh cũ ở cuối
            z (Edge): Cạnh mới

        Returns:
            bool: True nếu cạnh cũ được thay đổi, nếu không là False
        """
        
        if self.edges[-1] == x:
            self.edges[-1] = z
            
            # Thêm read hiện tại và tập các read của cạnh mới
            z.reads.append(self)
            
            # Xóa read hiện tại từ cạnh cũ
            if self in x.reads:
                x.reads.remove(self)
                
            return True
        
        return False
    
    
    def change_y(self, y: Edge, z: Edge) -> bool:
        """Thay đổi cạnh đầu tiên trong tập các cạnh của read hiện tại thành cạnh mới z nếu cạnh đầu tiên là y

        Args:
            y (Edge): Cạnh cũ ở đầu
            z (Edge): Cạnh mới

        Returns:
            bool: True nếu cạnh cũ được thay đổi, nếu không là False
        """
        if self.edges[0] == y:
            self.edges[0] = z
            
            # Thêm read hiện tại và tập các read của cạnh mới
            z.reads.append(self)
            
            # Xóa read hiện tại từ cạnh cũ
            if self in y.reads:
                y.reads.remove(self)
                
            return True
        
        return False
    
    
    def change_xy(self, x: Edge, y: Edge, z: Edge) -> bool:
        """Thay đổi hai cạnh liên tiếp x, y trong đường dẫn
    

        Args:
            x (Edge): Cạnh đầu tiên liền trước
            y (Edge): Cạnh liền sau cạnh x
            z (Edge): Cạnh mới thay thế hai cạnh x và cạnh y

        Returns:
            bool: True nếu hai cạnh bị thay đổi bởi z, nếu không là False
        """
        
        found_xy: bool = False
        
        # Xét từng cặp cạnh liền nhau có phải là cạnh x là cạnh đầu tiên, y là cạnh liền cạnh x hay không:
        for i in range(len(self.edges)-1):
            
            # Nếu tìm thấy x là cạnh liền trước, y là cạnh liền sau cạnh x
            if self.edges[i] == x and self.edges[i+1] == y:
                found_xy = True
                
                # Thêm cạnh z, xóa bỏ các cạnh x và cạnh y
                self.edges[i] = z
                self.edges[i+1] = None
                
                # Thêm read hiện tại vào danh sách các read của cạnh mới z
                z.reads.append(self)
                
                # Xóa read hiện tại từ danh sách các read của các cạnh bị xóa x và y
                if self in x.reads:
                    x.reads.remove(self)
                if self in y.reads:
                    y.reads.remove(self)
        
        # Xóa tất cả các cạnh mà vị trí đó là None
        self.edges = [e for e in self.edges if e != None]
        
        return found_xy
    
    
    def update(self, x: Edge, y: Edge, z: Edge) -> bool:
        """Chạy tất cả các phương thức cập nhật cạnh mới

        Args:
            x (Edge): Cạnh nếu là cạnh cuối cùng trong danh sách các cạnh sẽ bị thay thế bởi cạnh z
            y (Edge): Cạnh nếu là cạnh đầu tiên trong danh sách các cạnh sẽ bị thay thế bởi cạnh z
            z (Edge): Cạnh mới

        Returns:
            bool: True nếu có thay đổi, nếu không là False
        """
        
        # Xét từng trường hợp
        changed: List[bool] = [self.change_xy(x=x, y=y, z=z), self.change_x(x=x, z=z), self.change_y(y=y, z=z)]
        
        return any(changed)
    
    
class Graph(object):
    
    def __init__(self, seqs: Optional[Loader], k: int, threshold: int, error_correct: bool = False) -> None:
        """

        Args:
            seqs (Loader): Các reads đọc được trong loader
            k (int): k-mers, số ký tự trong một chuỗi đại diện cho một cạnh
            threshold (int): ngưỡng để sửa lỗi
            error_correct (bool, optional): Có sử lỗi hay không. Defaults to False.
        """
        
        self.vertex_list: List[Vertex] = [] # Danh sách các đỉnh trong đồ thị
        self.vertex_dict: Dict[str, Vertex] = {} # Danh sách các đỉnh được đánh chỉ mục bởi chuỗi đại diện
        self.edge_list: List[Edge] = [] # Danh sách các cạnh trong đồ thị
        self.edge_dict: Dict[str, Edge] = {} # Danh sách các cạnh trong đồ thị được chỉ mục bởi chuỗi đại diện
        self.read_list: List[Read] = [] # Danh sách các reads trong đồ thị
        self.k: int = k # Độ dài chuỗi đại diện cho một cạnh
        self.seqs: Optional[Loader] = seqs # Các read được đọc từ loader
        self.threshold: int = threshold # Ngưỡng để sửa lỗi
        
        
        for s in range(len(seqs)):
            # Lấy các read
            seq: str = seqs[s]
            # Tạo object Read
            read: Read = Read(sequence=seq, read_id=s)
            self.read_list.append(read)
            
            # Tạo các đỉnh và các cạnh
            for i in range(len(seq)-k+1):
                # Tạo k-mer
                k_mer: str = seq[i:i+k]
                prefix: str = k_mer[:k-1]
                suffix: str = k_mer[1:]
                
                # Tạo đỉnh tiền tố
                if prefix in self.vertex_dict:
                    p_vertex: Vertex = self.vertex_dict[prefix]
                else:
                    p_vertex: Vertex = self.new_vertex(sequence=prefix)
                
                # Tạo đỉnh hậu tố
                if suffix in self.vertex_dict:
                    s_vertex: Vertex = self.vertex_dict[suffix]
                else:
                    s_vertex: Vertex = self.new_vertex(sequence=suffix)
                    
                # Tạo cạnh
                if k_mer in self.edge_dict:
                    edge: Edge = self.edge_dict[k_mer]
                else:
                    edge: Edge = self.new_edge(in_vertex=p_vertex, out_vertex=s_vertex, sequence=k_mer)
                    
                # Thêm cạnh vào danh sách cạnh của read
                read.edges.append(edge)
                # Thêm read vào danh sách read của cạnh
                edge.reads.append(read)
                
        for i, vertex in enumerate(self.vertex_list):
            print(i, vertex, len(vertex.out_edges) - len(vertex.in_edges))
                
                
    def __str__(self) -> str:
        """_summary_

        Returns:
            str: In ra các cạnh và các đỉnh kề
        """
        
        out: str = ""
        for edge in self.edge_list:
            out = out + str(edge) + ": " + str(edge.in_vertex) + ", " + str(edge.out_vertex) + "\n"
            
        return out
    
    
    def new_vertex(self, sequence: str) -> Vertex:
        """Tạo ra một đỉnh mới thêm vào đồ thị

        Args:
            sequence (str): Chuỗi đại diện cho đỉnh

        Returns:
            Vertex: Đỉnh mới được tạo ra
        """
        
        vertex: Vertex = Vertex(sequence=sequence)
        self.vertex_list.append(vertex)
        self.vertex_dict[sequence] = vertex
        
        return vertex
    
    
    def new_edge(self, in_vertex: Vertex, out_vertex: Vertex, sequence: str) -> Edge:
        """Tạo ra một cạnh mới thêm vào đồ thị khi cho biết đỉnh vào, đỉnh ra, chuỗi đại diện cho cạnh

        Args:
            in_vertex (Vertex): Đỉnh vào cạnh mới
            out_vertex (Vertex): Đỉnh ra cạnh mới
            sequence (str): Chuỗi đại diện cho cạnh mới

        Returns:
            Edge: Cạnh mới được tạo ra
        """
        
        edge: Edge = Edge(in_vertex=in_vertex, out_vertex=out_vertex, sequence=sequence)
        self.edge_list.append(edge)
        in_vertex.add_out_edge(out_vertex=out_vertex, edge=edge)
        self.edge_dict[sequence] = edge
        
        return edge
    

    def merge(self, x: Edge, y: Edge) -> Edge:
        """Gộp hai cạnh kề nhau x và y

        Args:
            x (Edge): Cạnh liền trước
            y (Edge): Cạnh liền sau

        Returns:
            Edge: Cạnh kết quả là cạnh được gộp hai cạnh x và cạnh y
        """
        
        # Lấy các đỉnh là đỉnh vào của cạnh x, đỉnh ra của cạnh x và đỉnh ra của cạnh y
        in_vertex: Vertex = x.in_vertex
        mid_vertex: Vertex = x.out_vertex
        out_vertex: Vertex = y.out_vertex
        
        assert mid_vertex == y.in_vertex
        
        # Kiểm tra các đỉnh vẫn còn kích hoạt (không có đỉnh nào không có cạnh vào hoặc cạnh ra)
        
        if len(in_vertex.out_edges) == 0 or len(mid_vertex.in_edges) == 0 or \
            len(mid_vertex.out_edges) == 0 or len(out_vertex.in_edges) == 0:
                return None
            
        # Tạo chuỗi đại diện mới cho cạnh mới        
        y_length: int = len(y.sequence)
        seq: str = x.sequence + y.sequence[self.k-1:]
        
        # Tạo một cạnh mới        
        z: Edge = self.new_edge(in_vertex=in_vertex, out_vertex=out_vertex, sequence=seq)
        
        # Cập nhật các đỉnh và đường đi
        if x in in_vertex.out_edges:
            in_vertex.out_edges.remove(x)
        if x in mid_vertex.in_edges:
            mid_vertex.in_edges.remove(x)
        if y in mid_vertex.out_edges:
            mid_vertex.out_edges.remove(y)
        if y in out_vertex.in_edges:
            out_vertex.in_edges.remove(y)
        for read in self.read_list:
            read.update(x=x, y=y, z=z)
            
        return z
    
    
    def clean(self) -> None:
        """Loại bỏ các cạnh và đỉnh trống từ đồ thị
        """
        
        # Loại bỏ các đỉnh rỗng
        to_remove_vertex: List[Vertex] = []
        for vertex in self.vertex_list:
            if len(vertex.in_edges) == 0 and len(vertex.out_edges) == 0:
                to_remove_vertex.append(vertex)
                
        # Xóa các đỉnh rỗng
        for vertex in to_remove_vertex:
            self.vertex_list.remove(vertex)
            
        # Loại bỏ các cạnh rỗng
        to_remove_edge: List[Edge] = []
        for edge in self.edge_list:
            if len(edge.reads) == 0:
                to_remove_edge.append(edge)
            elif edge.in_vertex not in self.vertex_list:
                to_remove_edge.append(edge)
            elif edge.out_vertex not in self.vertex_list:
                to_remove_edge.append(edge)
                
        # Xóa các cạnh rỗng
        for edge in to_remove_edge:
            self.edge_list.remove(edge)
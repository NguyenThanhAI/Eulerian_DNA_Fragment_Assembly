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
    

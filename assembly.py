from loader import Loader
from graph import *


class Assembler(object):
    def __init__(self, filename: str, k: int, error_correct: bool=False) -> None:
        """Khởi tạo Assembler

        Args:
            filename (str): File chứa các read
            k (int): Độ dài một k-mer
            error_correct (bool, optional): Có sửa lỗi hay không. Defaults to False.
        """
        
        # Load file
        reads: Loader = Loader.load(filename=filename)
        
        # Khởi tạo đồ thị
        self.graph: Graph = Graph(seqs=reads, k=k, threshold=error_correct)
        self.k: int = k
        
        
    def superpath_consider(self) -> bool:
        """Gộp các cạnh nếu có thể

        Returns:
            bool: Có thể gộp được hai cạnh nào đó không
        """
        for vertex in self.graph.vertex_list:
            num_in_edge: int = len(vertex.in_edges)
            num_out_edge: int = len(vertex.out_edges)
            if (num_in_edge == 0 or num_out_edge == 0) and abs(num_in_edge - num_out_edge) == 1:
                continue
            in_edges: List[Edge] = vertex.in_edges
            out_edges: List[Edge] = vertex.out_edges
            if num_in_edge == num_out_edge:
                if num_in_edge == 1:
                    x: Edge = in_edges[0]
                    y: Edge = out_edges[1]
                    for read in x.reads:
                        # Kiểm tra x và y có cùng một read
                        if y in read:
                            
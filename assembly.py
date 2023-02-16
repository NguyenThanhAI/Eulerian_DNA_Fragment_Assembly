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
        
        
    def make_superpath(self) -> None:
        self.merge_single_edges()
        self.merge_multiple_edges()
        
        
    def merge_single_edges(self) -> None:
        """Gộp các cạnh nếu có thể

        Returns:
            bool: Có thể gộp được hai cạnh nào đó không
        """
        vertex_list: List[Vertex] = self.graph.vertex_list.copy()
        #for vertex in self.graph.vertex_list:
        while len(vertex_list) != 0:
            vertex: Vertex = vertex_list.pop(0)
            num_in_edge: int = len(vertex.in_edges)
            num_out_edge: int = len(vertex.out_edges)
            # Đỉnh đầu hoặc đỉnh kết thúc nên bỏ qua
            if (num_in_edge == 0 or num_out_edge == 0) and abs(num_in_edge - num_out_edge) == 1:
                continue
            # Đỉnh đã bị loại bỏ
            if num_in_edge == 0 and num_out_edge == 0:
                continue
            in_edges: List[Edge] = vertex.in_edges.copy()
            out_edges: List[Edge] = vertex.out_edges.copy()
            # Nếu là đỉnh cân bằng, ta xét xem có thể gộp các cạnh vào và cạnh ra được không
            if num_in_edge == num_out_edge:
                #if num_in_edge == 1:
                # So sánh từng cạnh với nhau
                for x in in_edges:
                    x_reads = x.reads.copy()
                    for y in out_edges:
                        # Kiểm tra từng read trong x xem x có thuộc vào read nào trong y hay không
                        for read in x_reads:
                            # Kiểm tra x và y có cùng một read
                            if read in y.reads:
                                # Kiểm tra x và y có liền kề nhau trong read này hay không
                                if read.check_consecutive_edges(x=x, y=y):
                                    if self.graph.merge(x=x, y=y):
                                        self.graph.clean()
                                    
        self.graph.clean()
        
        
    def merge_multiple_edges(self) -> None:
        """
        Gộp các cạnh bội
        """
        vertex_list: List[Vertex] = self.graph.vertex_list.copy()
        while len(vertex_list) != 0:
            vertex: Vertex = vertex_list.pop(0)
            num_in_edge: int = len(vertex.in_edges)
            num_out_edge: int = len(vertex.out_edges)
            diff: int = num_out_edge - num_in_edge
            if (num_in_edge == 0 or num_out_edge == 0) and abs(diff) == 1:
                continue
            if num_in_edge == 0 and num_out_edge == 0:
                continue
            #assert diff != 0, print(vertex)
            in_edges: List[Edge] = vertex.in_edges.copy()
            out_edges: List[Edge] = vertex.out_edges.copy()
            for x in in_edges:
                x_reads = x.reads.copy()
                for y in out_edges:
                    for read in x_reads:
                        if read in y.reads:
                            if read.check_consecutive_edges(x=x, y=y):
                                print("{} và {} gộp được".format(x.sequence, y.sequence))
                                if self.graph.merge_mul(x=x, y=y):
                                    self.graph.clean()
                                    break
        
    
    def is_eulerian(self) -> bool:
        """
        Kiểm tra đồ thị có phải là đồ thị Euler hay không

        Returns:
            bool: Nếu là đồ thị Euler trả về True, nếu không là False
        """
        non_bal: int = 0
        diff_list: List[int] = []
        for i, vertex in enumerate(self.graph.vertex_list):
            diff = len(vertex.out_edges) - len(vertex.in_edges)
            if diff != 0:
                non_bal += 1
                '''in_degree: int = 0
                for in_edge in vertex.in_edges:
                    in_degree += in_edge.multiplicities
                out_degree: int = 0
                for out_edge in vertex.out_edges:
                    out_degree += out_edge.multiplicities'''
                diff_mul = vertex.compute_degree()
                print(i, vertex, diff)
                diff_list.append(diff_mul)
            
        
        if all(d == 0 for d in diff_list[1:-1]) and diff_list[0] * diff_list[-1] == -1:
            return True
        else:
            return False
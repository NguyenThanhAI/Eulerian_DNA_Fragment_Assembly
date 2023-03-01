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
            '''if (num_in_edge == 0 or num_out_edge == 0) and abs(num_in_edge - num_out_edge) == 1:
                continue'''
            if abs(vertex.compute_degree()) == 1:
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
                        if x.multiplicities == y.multiplicities:
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
            '''if (num_in_edge == 0 or num_out_edge == 0) and abs(diff) == 1:
                continue'''
            if abs(vertex.compute_degree()) == 1:
                continue
            if num_in_edge == 0 and num_out_edge == 0:
                continue
            #assert diff != 0, print(vertex)
            in_edges: List[Edge] = vertex.in_edges.copy()
            out_edges: List[Edge] = vertex.out_edges.copy()
            print("=============================={}=======================================".format(vertex))
            for x in in_edges:
                if x.multiplicities == 0:
                    continue
                x_reads = x.reads.copy()
                for y in out_edges:
                    if x.multiplicities == 0 or y.multiplicities == 0 or x == y:
                        continue
                    for read in x_reads:
                        if read in y.reads:
                            if read.check_consecutive_edges(x=x, y=y):
                                print("{} và {} gộp được".format(x.sequence, y.sequence), end=" ")
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
                
                print(i, vertex, diff)
                
            diff_mul = vertex.compute_degree()
            if diff_mul == 0:
                continue
            else:
                if abs(diff_mul) >= 2:
                    return False
                else:
                    diff_list.append(diff_mul)
            
        
        if len(diff_list) == 2 and diff_list[0] * diff_list[-1] == -1:
            return True
        else:
            return False
        
        
    def dfs_visit(self, path: List[Edge], vertex: Vertex, end_vertex: Vertex) -> Tuple[List[Edge], bool, bool]:
        
        out_edges: List[Edge] = vertex.out_edges
        for o_edge in out_edges:
            if (o_edge.visited < o_edge.multiplicities):
                o_edge.visited += 1
                path.append(o_edge)
                all_visited: bool = self.graph.check_all_visited()
                o_vertex: Vertex = o_edge.out_vertex
                if all_visited and o_vertex == end_vertex:
                    return path, all_visited, o_vertex == end_vertex
                else:
                    if o_vertex != end_vertex:
                        path, all_visited, end_equal = self.dfs_visit(path=path, vertex=o_vertex, end_vertex=end_vertex)
                        if all_visited and end_equal:
                            return path, all_visited, end_equal
                    else:
                        path.remove(o_edge)
                        o_edge.visited -= 1
    
    
    def find_eulerian_path(self) -> str:
        start_vertex: Vertex = None
        end_vertex: Vertex = None
        for vertex in self.graph.vertex_list:
            if vertex.compute_degree() == 1:
                start_vertex = vertex
            if vertex.compute_degree() == -1:
                end_vertex = vertex
        path: List[Edge] = []   
        path, all_visited, end_equal = self.dfs_visit(path=path, vertex=start_vertex, end_vertex=end_vertex)
        assert all_visited and end_equal
        origin_string: str = ""
        for i, edge in enumerate(path):
            if i == 0:
                origin_string += edge.sequence
            else:
                origin_string += edge.sequence[self.graph.k - 1:]
                
        return origin_string
    
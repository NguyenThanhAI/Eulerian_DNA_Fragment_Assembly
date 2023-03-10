from assembly import Assembler


if __name__ == "__main__":   
    assembly: Assembler = Assembler(filename=r"data/paper_example_8.fastq", k=8)
    print(assembly.is_eulerian())
    #print(assembly.graph)
    assembly.make_superpath()
    print(assembly.is_eulerian())
    print("===================================================")
    print(assembly.graph)
    print("===================================================")
    if assembly.is_eulerian():
        print("Số đường đi Euler có thể là: {}".format(assembly.graph.get_numbers_eulerian_path()))
        origin_string = assembly.find_eulerian_path()
        print("Dãy ban đầu là: {}".format(origin_string))
    else:
        print("Đồ thị không phải là đồ thị Euler")
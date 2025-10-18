import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt

# A Python tool with a graphical interface for visualizing, analyzing, and testing properties of binary relations.
# Built with Tkinter and NetworkX, this app allows users to input a relation, visualize its graph, examine strict
# and indifference parts, and check key properties and topological sorts.
# This was built with the support of Cursor AI.

class BinaryRelationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Binary Relation Visualizer")
        self.root.geometry("700x700")
        self.root.configure(bg="#f4f4f9")

        self.size = None
        self.entries = []

        self.setup_size_input()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def setup_size_input(self):
        """Initial screen to enter number of elements."""
        self.clear_window()

        tk.Label(
            self.root,
            text="Binary Relation Visualizer",
            font=("Helvetica", 20, "bold"),
            bg="#f4f4f9",
            fg="#333"
        ).pack(pady=20)

        tk.Label(
            self.root,
            text="Enter number of elements (3-10):",
            font=("Helvetica", 12),
            bg="#f4f4f9"
        ).pack(pady=10)

        self.size_entry = tk.Entry(self.root, font=("Helvetica", 12), justify="center", width=10)
        self.size_entry.pack(pady=5)

        tk.Button(
            self.root,
            text="Next",
            command=self.create_matrix_input,
            font=("Helvetica", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            width=12,
            relief="flat",
            cursor="hand2"
        ).pack(pady=15)

    def create_matrix_input(self):
        try:
            m = int(self.size_entry.get())
            if not (3 <= m <= 10):
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter an integer between 3 and 10.")
            return

        self.size = m
        self.clear_window()

        tk.Label(
            self.root,
            text=f"Enter Relation Matrix ({m}×{m})",
            font=("Helvetica", 16, "bold"),
            bg="#f4f4f9",
            fg="#222"
        ).pack(pady=15)

        frame = tk.Frame(self.root, bg="#f4f4f9")
        frame.pack()

        # Add column labels 
        for j in range(m):
            tk.Label(
                frame,
                text=chr(97 + j),
                font=("Helvetica", 12, "bold"),
                bg="#f4f4f9"
            ).grid(row=0, column=j+1, padx=8)

        self.entries = []
        for i in range(m):
            # Add row label
            tk.Label(
                frame,
                text=chr(97 + i),
                font=("Helvetica", 12, "bold"),
                bg="#f4f4f9"
            ).grid(row=i+1, column=0, padx=8)
            row = []
            for j in range(m):
                var = tk.IntVar()
                chk = tk.Checkbutton(
                    frame,
                    variable=var,
                    bg="#f4f4f9",
                    activebackground="#dfffd8",
                    onvalue=1,
                    offvalue=0,
                    width=3,
                    height=1
                )
                chk.grid(row=i+1, column=j+1, padx=8, pady=8)
                row.append(var)
            self.entries.append(row)

        btn_frame = tk.Frame(self.root, bg="#f4f4f9")
        btn_frame.pack(pady=20)

        tk.Button(
            btn_frame,
            text="Visualize Graph",
            command=self.visualize_relation,
            font=("Helvetica", 12, "bold"),
            bg="#2196F3",
            fg="white",
            width=15,
            relief="flat",
            cursor="hand2"
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            btn_frame,
            text="Show Strict Relation",
            command=self.visualize_strict_relation,
            font=("Helvetica", 12, "bold"),
            bg="#FF9800",
            fg="white",
            width=20,
            relief="flat",
            cursor="hand2"
        ).grid(row=0, column=1, padx=10)

        tk.Button(
            btn_frame,
            text="Show Indifference Relation",
            command=self.visualize_indifference_relation,
            font=("Helvetica", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            width=25,
            relief="flat",
            cursor="hand2"
        ).grid(row=0, column=2, padx=10)

        tk.Button(
            btn_frame,
            text="Back",
            command=self.setup_size_input,
            font=("Helvetica", 12, "bold"),
            bg="#E53935",
            fg="white",
            width=10,
            relief="flat",
            cursor="hand2"
        ).grid(row=0, column=3, padx=10)
        
        self.create_property_buttons()
        
    def get_relation_matrix(self):
        return [[self.entries[i][j].get() for j in range(self.size)] for i in range(self.size)]

    def visualize_relation(self):
        R = self.get_relation_matrix()

        G = nx.DiGraph()

        # Add nodes and edges
        for i in range(self.size):
            G.add_node(chr(97 + i))
        for i in range(self.size):
            for j in range(self.size):
                if R[i][j] == 1:
                    G.add_edge(chr(97 + i), chr(97 + j))

        plt.figure(figsize=(7, 6))
        pos = nx.spring_layout(G, seed=42, k=1)
        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color="#90CAF9",
            node_size=1500,
            font_size=12,
            font_weight="bold",
            arrowsize=20,
            edgecolors="#0D47A1"
        )
        plt.title("Graph of Relation R", fontsize=14, fontweight="bold")
        
        ax = plt.gca()
        plt.show()

    # ====================
    # TOPOLOGICAL SORTING
    # ====================

    def Topologicalsorting1(self):
        R = self.StrictRelation()
        m = len(R)

        # Build the directed graph
        G = nx.DiGraph()
        G.add_nodes_from(range(m))
        for i in range(m):
            for j in range(m):
                if R[i][j] == 1:
                    G.add_edge(i, j)

        # Check for cycles 
        if not nx.is_directed_acyclic_graph(G):
            raise ValueError("Relation has cycles. Topological sorting 1 not possible.")

        return list(nx.topological_sort(G))

    def Topologicalsorting2(self):
        R = self.get_relation_matrix()
        m = len(R)

        # Validate that both symmetric and asymmetric parts are non-empty
        sym = self.IndifferenceRelation()
        strict = self.StrictRelation()

        def has_any_one(M):
            for row in M:
                for v in row:
                    if v == 1:
                        return True
            return False

        if not has_any_one(sym) or not has_any_one(strict):
            raise ValueError("Symmetric and asymmetric parts are empty. Topological sorting 2 not possible.")

        # Build undirected graph for symmetric edges to find equivalence classes
        parent = list(range(m))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(x, y):
            rx, ry = find(x), find(y)
            if rx != ry:
                parent[ry] = rx

        for i in range(m):
            for j in range(i + 1, m):
                if R[i][j] == 1 and R[j][i] == 1:
                    union(i, j)

        # Make node groups
        rep_to_members = {}
        for i in range(m):
            r = find(i)
            rep_to_members.setdefault(r, []).append(i)

        reps = list(rep_to_members.keys())
        k = len(reps)

        # Build DAG using asymmetric edges only
        class_index = {rep: idx for idx, rep in enumerate(reps)}
        G = nx.DiGraph()
        for ra in reps:
            a_idx = class_index[ra]
            for rb in reps:
                if ra == rb:
                    continue
                for i in rep_to_members[ra]:
                    for j in rep_to_members[rb]:
                        if self.StrictRelation()[i][j] == 1:
                            G.add_edge(a_idx, class_index[rb])
                            break

        condensed = nx.condensation(G)
        topo_sccs = list(nx.topological_sort(condensed))

        result = []
        for scc_idx in topo_sccs:
            scc = condensed.nodes[scc_idx]['members']
            group = []
            for class_idx in scc:
                rep = reps[class_idx]
                group.extend(sorted(rep_to_members[rep]))
            result.append(sorted(group))
        return result


    # ====================
    # PROPERTY CHECKS
    # ====================

    def CompleteCheck(self):
        R = self.get_relation_matrix()
        m = len(R)
        for i in range(m):
            for j in range(m):
                if i != j and R[i][j] == 0 and R[j][i] == 0:
                    return False, (chr(97 + i), chr(97 + j))
        return True, None

    def ReflexiveCheck(self):
        R = self.get_relation_matrix()
        m = len(R)
        for i in range(m):
            if R[i][i] == 0:
                return False, i
        return True, None

    def AsymmetricCheck(self):
        R = self.get_relation_matrix()
        m = len(R)
        for i in range(m):
            for j in range(m):                
                if R[i][j] == 1 and R[j][i] == 1:
                    return False, (chr(97 + i), chr(97 + j))
        return True, None

    def SymmetricCheck(self):
        R = self.get_relation_matrix()
        m = len(R)
        for i in range(m):
            for j in range(m):
                if R[i][j] == 1 and R[j][i] == 0:
                    return False, (chr(97 + i), chr(97 + j))
        return True, None

    def AntisymmetricCheck(self):
        R = self.get_relation_matrix()
        m = len(R)
        for i in range(m):
            for j in range(m):
                if i != j and R[i][j] == 1 and R[j][i] == 1:
                    return False, (chr(97 + i), chr(97 + j))
        return True, None

    def TransitiveCheck(self):
        R = self.get_relation_matrix()
        m = len(R)
        for i in range(m):
            for j in range(m):
                if R[i][j] == 1:
                    for k in range(m):
                        if R[j][k] == 1 and R[i][k] == 0:
                            return False, (chr(97 + i), chr(97 + j), chr(97 + k))
        return True, None

    def NegativeTransitiveCheck(self):
        R = self.get_relation_matrix()
        m = len(R)
        for i in range(m):
            for j in range(m):
                if R[i][j] == 0:
                    for k in range(m):
                        if R[j][k] == 0 and R[i][k] == 1:
                            return False, (chr(97 + i), chr(97 + j), chr(97 + k))
        return True, None

    def CompleteOrderCheck(self):
        c, _ = self.CompleteCheck()
        t, _ = self.TransitiveCheck()
        a, _ = self.AntisymmetricCheck()
        return c and t and a, None

    def CompletePreOrderCheck(self):
        c, _ = self.CompleteCheck()
        t, _ = self.TransitiveCheck()
        return c and t, None

    def StrictRelation(self):
        R = self.get_relation_matrix()
        m = len(R)
        A = [[0]*m for _ in range(m)] 
        for i in range(m): 
            for j in range(m): 
                if R[i][j] == 1 and R[j][i] == 0: 
                    A[i][j] = 1 
        return A 
    
    def IndifferenceRelation(self): 
        R = self.get_relation_matrix()
        m = len(R)
        A = [[0]*m for _ in range(m)]
        for i in range(m): 
            for j in range(m): 
                if R[i][j] == 1 and R[j][i] == 1: 
                    A[i][j] = 1 
        return A

    def visualize_strict_relation(self):
        R = self.StrictRelation()
        G = nx.DiGraph()
        
        # Add nodes and edges
        for i in range(self.size):
            G.add_node(chr(97 + i))
        for i in range(self.size):
            for j in range(self.size):
                if R[i][j] == 1:
                    G.add_edge(chr(97 + i), chr(97 + j))
        
        plt.figure(figsize=(7, 6))
        pos = nx.spring_layout(G, seed=42, k=1)
        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color="#FFB74D",
            node_size=1500,
            font_size=12,
            font_weight="bold",
            arrowsize=20,
            edgecolors="#E65100"
        )
        plt.title("Strict Relation - Asymmetric Part", fontsize=14, fontweight="bold")
        
        ax = plt.gca()
        plt.show()

    def visualize_indifference_relation(self):
        R = self.IndifferenceRelation()
        G = nx.DiGraph()

        # Add nodes and all directed edges, including self-loops
        for i in range(self.size):
            G.add_node(chr(97 + i))
        for i in range(self.size):
            for j in range(self.size):
                if R[i][j] == 1:
                    G.add_edge(chr(97 + i), chr(97 + j))

        plt.figure(figsize=(7, 6))
        pos = nx.spring_layout(G, seed=42)
        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color="#81C784",
            node_size=1500,
            font_size=12,
            font_weight="bold",
            arrowsize=20,
            edgecolors="#2E7D32"
        )
        plt.title("Indifference Relation - Symmetric Part", fontsize=14, fontweight="bold")

        ax = plt.gca()
        plt.show()

    # ====================
    # UI
    # ====================

    def create_property_buttons(self):
        frame = tk.Frame(self.root, bg="#f4f4f9")
        frame.pack(pady=10)

        properties = [
            ("Reflexive", self.ReflexiveCheck),
            ("Symmetric", self.SymmetricCheck),
            ("Antisymmetric", self.AntisymmetricCheck),
            ("Asymmetric", self.AsymmetricCheck),
            ("Transitive", self.TransitiveCheck),
            ("Negative Transitive", self.NegativeTransitiveCheck),
            ("Complete", self.CompleteCheck),
            ("Complete Order", self.CompleteOrderCheck),
            ("Complete Preorder", self.CompletePreOrderCheck),
        ]

        for i, (label, func) in enumerate(properties):
            tk.Button(
                frame,
                text=label,
                font=("Helvetica", 11),
                bg="#FFC107",
                fg="black",
                relief="flat",
                width=18,
                command=lambda f=func, name=label: self.check_property(f, name)
            ).grid(row=i // 3, column=i % 3, padx=8, pady=8)

        # Buttons for topological sorting
        tk.Button(
            frame,
            text="Topological sorting 1",
            font=("Helvetica", 11),
            bg="#8BC34A",
            fg="black",
            relief="flat",
            width=18,
            command=self.show_toposort1
        ).grid(row=(len(properties)) // 3, column=0, padx=8, pady=8)

        tk.Button(
            frame,
            text="Topological sorting 2",
            font=("Helvetica", 11),
            bg="#CDDC39",
            fg="black",
            relief="flat",
            width=18,
            command=self.show_toposort2
        ).grid(row=(len(properties)) // 3, column=1, padx=8, pady=8)


    def check_property(self, func, name):
        result, example = func()
        if result:
            messagebox.showinfo("Property Check", f"The relation is {name}.")
        else:
            message = f"The relation is NOT {name}."
            if example:
                message += f"\nCounterexample: {example}"
            messagebox.showwarning("Property Check", message)

    def show_toposort1(self):
        try:
            order = self.Topologicalsorting1()
            labels = [chr(97 + i) for i in order]
            messagebox.showinfo("Topological Sorting 1", " - ".join(labels))
        except ValueError as e:
            messagebox.showerror("Topological Sorting 1", str(e))

    def show_toposort2(self):
        try:
            classes = self.Topologicalsorting2()
            parts = []
            for cls in classes:
                labels = ", ".join(chr(97 + i) for i in cls)
                parts.append(f"[{labels}]")
            messagebox.showinfo("Topological Sorting 2", " - ".join(parts))
        except ValueError as e:
            messagebox.showerror("Topological Sorting 2", str(e))

root = tk.Tk()
app = BinaryRelationApp(root)
root.mainloop()

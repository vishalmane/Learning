using System;

namespace Iterator
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Hello World!");
            var tree = new Node<int>(1)
            {
                Left = new Node<int>(2)
                {
                    Left = new Node<int>(4),
                    Right = new Node<int>(5)
                },
                Right = new Node<int>(3)
            };
            var iterator = new DepthFirstIterator<int>(tree);
            while (!iterator.IsDone())
            {
                iterator.GetNextValue();
            }
        }
    }

    public class Node<T>
    {
        public Node<T> Left;
        public Node<T> Right;
        public Node<T> Parent;
        public T Value;

        public Node(T value)
        {
            Value = value;
        }

        public Node(Node<T> left, Node<T> right, T value)
        {
            Left = left;
            Right = right;
            Value = value;

            Left.Parent = this;
            Right.Parent = this;
        }


    }

    public interface IIterator<T>
    {
        Node<T> Current { get; set; }
        bool IsDone();
        T GetNextValue();
    }

    public class DepthFirstIterator<T>: IIterator<T>
    {
        public Node<T> Current { get; set; }
        public DepthFirstIterator(Node<T> root)
        {
            Current = root;
        }

       

        public T GetNextValue()
        {
            //Logic
            return Current.Value;
        }

        public bool IsDone()
        {
            if (Current.Right == null && Current.Left == null)
                return true;
            return false;
        }
    }
}

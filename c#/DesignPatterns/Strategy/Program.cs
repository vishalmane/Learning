using System;
using System.Collections.Generic;

namespace Strategy
{

    // The Strategy design pattern defines a family of algorithms, 
    // encapsulate each one, and make them interchangeable. 
    // This pattern lets the algorithm vary independently from clients that use it. 
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Hello World!");
            SortContext context= new SortContext(new SortByMarks(), new List<Student>());
            SortContext context1= new SortContext(new SortByRollNumber(), new List<Student>());
            SortContext context2= new SortContext(new SortByName(), new List<Student>());
        }
    }

    public class SortContext
    {
        private List<Student> Students { get; set; }
        private SortStrategy SortStrategy { get; set; }
        public SortContext(SortStrategy sortStrategy, List<Student> students)
        {
            SortStrategy = sortStrategy;
            Students = students;
        }

        public List<Student> Sort()
        {
            return SortStrategy.Sort(Students);
        }
    }

    public class Student
    {
        public string   Name { get; set; }
        public int   RollNumber { get; set; }
        public decimal Marks{ get; set; }
    }

    public abstract class SortStrategy
    {
        public abstract List<Student> Sort(List<Student> list);
    }

    public class SortByName : SortStrategy
    {
        public override List<Student> Sort(List<Student> list)
        {
            return list;
        }
    }
    public class SortByRollNumber : SortStrategy
    {
        public override List<Student> Sort(List<Student> list)
        {
            return list;

        }
    }
    public class SortByMarks : SortStrategy
    {
        public override List<Student> Sort(List<Student> list)
        {
            return list;

        }
    }
}

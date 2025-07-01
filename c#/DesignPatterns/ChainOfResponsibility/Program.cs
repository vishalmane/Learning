using System;

namespace ChainOfResponsibility
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Hello World!");
            var report = new Report("My Report", 1, 1);
            Console.WriteLine(report);

            var root = new CallHandler(report);
            
            root.Add(new PageHandler(report));
            root.Add(new HeightHandler(report));
            root.Add(new SubReportHandler(report));

            // eventually...
            root.Handle();
            Console.WriteLine(report);
        }
    }
}

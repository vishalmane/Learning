using System;

namespace Proxy
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Hello World!");
        }
    }

    public class Report{}
    public interface IReportDocument
    {
        public Report GetReport();
        public bool Printreport();
    }
    
    public class CRDocument : IReportDocument
    {
        public Report GetReport()
        {
            return new Report();
        }

        public bool Printreport()
        {
            return true;
        }
    }

    public class ReportProxy:IReportDocument
    {
        IReportDocument crReportDocument= new CRDocument();
        public Report GetReport()
        {
            //my logic
            return crReportDocument.GetReport();
        }

        public bool Printreport()
        {
            //my logic
            return crReportDocument.Printreport();
        }
    }
}

using System;
using System.Collections.Generic;
using System.Linq;

namespace Composite
{
    class Program
    {
        static void Main(string[] args)
        {
            BadReport badReport = new BadReport();
            badReport.SubReports = new List<BadReport>();
            var subrep1 = new BadReport() { Id = 1, Pages = 10 };
            var subrep2 = new BadReport() { Id = 1, Pages = 10, SubReports = new List<BadReport> { subrep1 } };
            var subrep3 = new BadReport() { Id = 1, Pages = 10 };
            var subrep4 = new BadReport() { Id = 1, Pages = 10 };
            badReport.SubReports.Add(subrep2);
            badReport.SubReports.Add(subrep3);
            badReport.SubReports.Add(subrep4);

            if (badReport != null)
            {
                foreach (var item in badReport.SubReports)
                {
                   
                }
            }



            Report report = new Report();
            var goodReport = new Report { Id = 1, Pages = 10 };
            report.Add(new Report { Id = 2, Pages = 5 });
            var total = report.TotalPages();
            report.Validate();            
        }
    }
    public class BadReport
    {
        public int Id { get; set; }
        public string Title { get; set; }
        public List<BadReport> SubReports { get; set; }
        public int Pages { get; set; }
    }
}

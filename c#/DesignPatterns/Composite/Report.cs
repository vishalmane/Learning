using System.Collections.Generic;
using System.Linq;

namespace Composite
{
    public class Report : BaseClass
    {
        public Report()
        {
            SubReports = new List<Report>();
        }
        public int Id { get; set; }
        public string Title { get; set; }
        public List<Report> SubReports { get; set; }
        public A a { get; set; }
        public B b { get; set; }
        public C c { get; set; }
        public D d { get; set; }

        public int Pages { get; set; }
        public void Add(Report report)
        {
            SubReports.Add(report);
        }
        public void Print()
        { }
        public int TotalPages()
        {
            int totalPages = 0;
            if (SubReports != null && SubReports.Any())
                SubReports.ForEach(r => totalPages = r.TotalPages() + Pages);
            return totalPages;
        }
        public List<BaseClass> ABCD { get; set; }

        public override bool Validate()
        {
            a.Validate();
            b.Validate();
            c.Validate();
            d.Validate();
            foreach (var item in ABCD)
            {
                item.Validate();
            }
            return true;
        }
    }
    public class A : BaseClass
    {
        public override bool Validate()
        {
            throw new System.NotImplementedException();
        }
    }
    public class B : BaseClass
    {
        public override bool Validate()
        {
            throw new System.NotImplementedException();
        }
    }
    public class C : BaseClass
    {
        public override bool Validate()
        {
            throw new System.NotImplementedException();
        }
    }
    public class D : BaseClass
    {
        public override bool Validate()
        {
            throw new System.NotImplementedException();
        }
    }

    public abstract class BaseClass
    {
        public abstract bool Validate();
    }
}

using System;

namespace ChainOfResponsibility
{
    public class PageHandler : CallHandler
    {
        public PageHandler(Report report)
            : base(report) { }

        public override void Handle()
        {
            if (Report.Pages == 0) throw new Exception("No Pages in Report");
            Console.WriteLine("Pages check Done!");
            base.Handle();
        }
    }
}
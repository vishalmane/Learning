using System;

namespace ChainOfResponsibility
{
    public class SubReportHandler : CallHandler
    {
        public SubReportHandler(Report report)
            : base(report) { }

        public override void Handle()
        {
            if (Report.SubReport != null)
            {
                //Do something
            }
            Console.WriteLine("SubReport check Done!");

            base.Handle();
        }
    }
}
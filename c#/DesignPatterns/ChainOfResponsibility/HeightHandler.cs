using System;

namespace ChainOfResponsibility
{
    public class HeightHandler : CallHandler
    {
        public HeightHandler(Report report)
            : base(report) { }

        public override void Handle()
        {
            // nothing
            if (Report.Height == 0) Report.Height = 100;
            Console.WriteLine("Height adjusted!");
            base.Handle();
        }
    }
}
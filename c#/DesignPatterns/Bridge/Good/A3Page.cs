using System;
using System.Collections.Generic;
using System.Text;

namespace Bridge.Good
{
    public class A3Page : Page
    {
        public A3Page(IPrinter printer) : base(printer)
        {
        }

        public override void PrintJob()
        {
            Printer.PrintJob();
        }
    }


}

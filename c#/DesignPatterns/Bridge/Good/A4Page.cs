namespace Bridge.Good
{
    public class A4Page : Page
    {
        public A4Page(IPrinter printer) : base(printer)
        {
        }

        public override void PrintJob()
        {
            Printer.PrintJob();
        }
    }


}

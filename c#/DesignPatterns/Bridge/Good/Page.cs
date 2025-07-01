namespace Bridge.Good
{
    public abstract class Page
    {
        public Page(IPrinter printer)
        {
            Printer = printer;
        }
        internal IPrinter Printer { get; set; }
        public abstract void PrintJob();
    }


}

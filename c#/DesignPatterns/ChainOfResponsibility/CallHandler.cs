namespace ChainOfResponsibility
{
    public class CallHandler
    {
        protected Report Report;
        protected CallHandler next;

        public CallHandler(Report report)
        {
            this.Report = report;
        }

        public void Add(CallHandler cm)
        {
            if (next != null) next.Add(cm);
            else next = cm;
        }

        public virtual void Handle() => next?.Handle();
    }
}
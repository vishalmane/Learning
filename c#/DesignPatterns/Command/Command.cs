namespace Command
{
    public abstract class Command
    {
        internal Job Job;

        protected Command(Job job)
        {
            Job = job;
        }
        public abstract bool Execute();
        public abstract bool ReExecute();
        public abstract bool Undo();

    }
}
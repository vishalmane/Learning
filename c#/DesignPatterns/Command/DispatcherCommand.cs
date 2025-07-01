using System;

namespace Command
{
    public class DispatcherCommand : Command
    {
        public override bool Execute()
        {
            Console.WriteLine("Dispatcher Command Execute");
            return true;
        }

        public override bool ReExecute()
        {
            Console.WriteLine("Dispatcher Command ReExecute");
            return true;

        }

        public override bool Undo()
        {
            Console.WriteLine("Dispatcher Command Undo");
            return true;

        }

        public DispatcherCommand(Job job) : base(job)
        {
        }
    }
}
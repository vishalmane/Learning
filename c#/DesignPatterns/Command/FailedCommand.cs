using System;

namespace Command
{
    public class FailedCommand : Command
    {
        public override bool Execute()
        {
            Console.WriteLine("Failed Command Execute");
            return true;
        }

        public override bool ReExecute()
        {
            Console.WriteLine("Failed Command ReExecute");
            return true;

        }

        public override bool Undo()
        {
            Console.WriteLine("Failed Command Undo");
            return true;

        }

        public FailedCommand(Job job) : base(job)
        {
        }
    }
}
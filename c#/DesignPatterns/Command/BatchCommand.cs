using System;

namespace Command
{
    public class BatchCommand : Command
    {
        public override bool Execute()
        {
            Console.WriteLine("Batch Command Execute");
            return true;
        }

        public override bool ReExecute()
        {
            Console.WriteLine("Batch Command ReExecute");
            return true;

        }

        public override bool Undo()
        {
            Console.WriteLine("Batch Command Undo");
            return true;

        }

        public BatchCommand(Job job) : base(job)
        {
        }
    }
}
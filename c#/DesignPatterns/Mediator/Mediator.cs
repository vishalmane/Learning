using System.Collections.Generic;

namespace Mediator
{
    public abstract class Mediator
    {
        internal List<WorkplaceComponent> WorkplaceComponents { get; set; }
        public abstract void Send(string message);
    }
}
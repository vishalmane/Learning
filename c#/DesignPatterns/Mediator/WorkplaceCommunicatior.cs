namespace Mediator
{
    public class WorkplaceCommunicatior : Mediator
    {
        public override void Send(string message)
        {
            WorkplaceComponents.ForEach(c=>c.OnMessageReceived(message));
        }
    }
}
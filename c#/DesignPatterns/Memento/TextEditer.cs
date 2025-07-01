namespace Memento
{
    public class TextEditer
    {
        public string Text { get; set; }
        public void ChangeText(string text)
        {
            Text = text;
        }
    }
}
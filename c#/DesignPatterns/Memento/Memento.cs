using System.Collections.Generic;

namespace Memento
{
    public class Memento
    {
        public List<string> Text { get; set; } = new List<string>();
        public int Current = 0;

        public void Save(string text)
        {
            Text.Add(text);
            Current++;
        }

        public string UnDo()
        {
            if (Current > 0)
                return Text[--Current];
            return string.Empty;
        }

        public string ReDo()
        {
            if (Current+1 < Text.Count)
                return Text[++Current];
            return string.Empty;
        }

    }
}
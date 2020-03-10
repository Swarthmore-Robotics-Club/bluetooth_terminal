import React, {Component} from 'react';
import {Editor, EditorState} from 'draft-js';


export default class Terminal extends Component{

    constructor(props){
        super(props)
        this.state = {editorState: EditorState.createEmpty()};
          this.onChange = (editorState) => this.setState({editorState});
          this.logState = () => console.log(this.state.editorState.toJS());
          this.setDomEditorRef = ref => this.domEditor = ref;
          this.focus = () => this.domEditor.focus();
    }
    
    componentDidMount(){
        this.domEditor.focus()
      }

      render() {
        const styles = {
            root: {
              fontFamily: '\'Helvetica\', sans-serif',
              padding: 20,
              width: window.innerWidth - window.innerWidth * .05,
              margin: 'auto',
            },
            editor: {
              border: '1px solid #ccc',
              cursor: 'text',
              minHeight: 80,
              padding: 10,
            },
            button: {
              marginTop: 10,
              textAlign: 'left',
            },
          };

          return (
            <div style={styles.root}>
              <div style={styles.editor} onClick={this.focus}>
                <Editor
                  editorState={this.state.editorState}
                  onChange={this.onChange}
                  placeholder="Enter some text..."
                  ref={this.setDomEditorRef}
                />
              </div>
              <input
                onClick={this.logState}
                style={styles.button}
                type="button"
                value="Log State"
              />
            </div>
          );
        }
}

import React from 'react';
import { AutoForm } from 'uniforms-semantic';
import { bridge as schema } from '../../schemas/PersonSchema.ts';
import 'semantic-ui-css/semantic.min.css';

const App: React.FC = () => <AutoForm schema={schema} onSubmit={console.log} />;

export default App;

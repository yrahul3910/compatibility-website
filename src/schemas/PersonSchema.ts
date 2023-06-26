import Ajv, { JSONSchemaType } from 'ajv';
import { JSONSchemaBridge } from 'uniforms-bridge-json-schema';

interface Person {
    // basics
    name: string,
    age: number,

    // work-related
    jobTitle: string,
    company: string,
    linkedinUrl: string,

    // personal
    hobbies: string[],
    favoriteMusicGenre: string,
    favoriteMusicArtist: string,
    favoriteMusicAlbum: string,
    favoriteCity: string,
    dietaryRestrictions: string[],

    // ideology
    politicalLeaning: string,
    religiousLeaning: string
}

const personSchema: JSONSchemaType<Person> = {
    title: 'Person',
    type: 'object',
    properties: {
        name: { type: 'string' },
        age: {
            type: 'integer',
            minimum: 18,
            maximum: 50
        },
        jobTitle: { type: 'string' },
        company: { type: 'string' },
        linkedinUrl: { type: 'string' },
        hobbies: {
            type: 'array',
            items: { type: 'string' }
        },
        favoriteMusicGenre: { type: 'string' },
        favoriteMusicArtist: { type: 'string' },
        favoriteMusicAlbum: { type: 'string' },
        favoriteCity: { type: 'string' },
        dietaryRestrictions: {
            type: 'array',
            items: { type: 'string' }
        },
        politicalLeaning: { type: 'string' },
        religiousLeaning: { type: 'string' }
    },
    required: [
        // eslint-disable-next-line array-element-newline
        'name', 'age', 'jobTitle', 'company', 'hobbies', 'favoriteMusicGenre', 'favoriteMusicArtist',
        'favoriteMusicAlbum', 'favoriteCity', 'dietaryRestrictions', 'politicalLeaning', 'religiousLeaning'
    ]
};

const ajv = new Ajv({
    allErrors: true,
    useDefaults: true,
    keywords: ['uniforms'],
});

function createValidator<T>(schema: JSONSchemaType<T>) {
    const validator = ajv.compile(schema);

    return (model: Record<string, unknown>) => {
        validator(model);
        return validator.errors?.length
            ? { details: validator.errors }
            : null;
    };
}

const schemaValidator = createValidator(personSchema);

export const bridge = new JSONSchemaBridge({
    schema: personSchema,
    validator: schemaValidator,
});
